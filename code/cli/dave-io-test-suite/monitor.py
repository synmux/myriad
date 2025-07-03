#!/usr/bin/env python3
"""Monitor script to test link redirects and email decoding on dave.io."""

from __future__ import annotations

import asyncio
import json
import sys
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse

import click
from playwright.async_api import ElementHandle, Page, Response, Route, async_playwright

# Global verbosity flag
_verbose = False


def log_message(message: str) -> None:
    """Log message to stderr if verbose mode is enabled."""
    if _verbose:
        print(message, file=sys.stderr)


@dataclass
class RedirectInfo:
    """Information about a single redirect."""

    from_url: str
    to_url: str
    status: int


@dataclass
class LinkTestResult:
    """Result of testing a single link."""

    link_index: int
    success: bool
    original_href: Optional[str] = None
    final_url: Optional[str] = None
    redirect_chain: List[RedirectInfo] = field(default_factory=list)  # type: ignore
    javascript_interference: bool = False
    external_redirect: bool = False
    aborted: bool = False
    error: Optional[str] = None


@dataclass
class EmailTestResult:
    """Result of testing email decoding."""

    success: bool
    final_text: Optional[str] = None
    replacement_time: Optional[int] = None
    error: Optional[str] = None


@dataclass
class TestSummary:
    """Summary statistics of test results."""

    successful: int
    failed: int
    external_redirects: int
    javascript_interference: int


@dataclass
class TestResults:
    """Complete test results."""

    success: bool
    total_links: int
    results: List[LinkTestResult]
    email_test: EmailTestResult
    summary: TestSummary
    error: Optional[str] = None


@dataclass
class FilteredLink:
    """A link that matches our filter criteria."""

    element: ElementHandle
    index: int
    href: str


@dataclass
class RedirectContext:
    """Context for tracking redirects during navigation."""

    redirect_chain: List[RedirectInfo] = field(default_factory=list)  # type: ignore
    external_redirect: bool = False
    aborted: bool = False


def is_internal_domain(url: str) -> bool:
    """Check if domain is internal (only dave.io)."""
    try:
        domain = urlparse(url).hostname
        return domain == "dave.io"
    except Exception:
        return False


def normalize_url(href: str, base_url: str) -> str:
    """Normalize URL to absolute form."""
    return href if href.startswith("http") else urljoin(base_url, href)


def is_go_link(url: str) -> bool:
    """Check if URL points to go links."""
    return url.startswith("https://dave.io/go/")


async def find_all_links(page: Page, link_selector: str) -> List[ElementHandle]:
    """Find all links matching the selector."""
    all_links = await page.query_selector_all(link_selector)
    if not all_links:
        raise ValueError(f"No links found matching selector: {link_selector}")
    return all_links


async def process_link_element(
    element: ElementHandle, index: int, base_url: str
) -> Optional[FilteredLink]:
    """Process a single link element and return if it matches criteria."""
    href = await element.get_attribute("href")
    if not href:
        return None

    absolute_href = normalize_url(href, base_url)
    if not is_go_link(absolute_href):
        return None

    return FilteredLink(element=element, index=index, href=absolute_href)


async def filter_go_links(
    all_links: List[ElementHandle], base_url: str
) -> List["FilteredLink"]:
    """Filter links to only those pointing to go links."""
    filtered_links: List[FilteredLink] = []

    for i, element in enumerate(all_links):
        if not element:
            continue

        processed_link = await process_link_element(element, i, base_url)
        if processed_link:
            filtered_links.append(processed_link)

    return filtered_links


def create_redirect_context() -> RedirectContext:
    """Create a new redirect context."""
    return RedirectContext()


def is_redirect_response(status: int) -> bool:
    """Check if status code indicates a redirect."""
    return 300 <= status < 400


def add_redirect_to_chain(
    response: Response, location: str, context: RedirectContext
) -> None:
    """Add a redirect to the chain."""
    context.redirect_chain.append(
        RedirectInfo(from_url=response.url, to_url=location, status=response.status)
    )


def process_redirect_location(location: str, context: RedirectContext) -> None:
    """Process redirect location to check if it's external."""
    if not (location and (location.startswith("http") or location.startswith("//"))):
        return

    redirect_url = f"https:{location}" if location.startswith("//") else location
    if not is_internal_domain(redirect_url):
        context.external_redirect = True


def handle_redirect_response(response: Response, context: RedirectContext) -> None:
    """Handle a redirect response."""
    if not is_redirect_response(response.status):
        return

    location = response.headers.get("location", "")
    add_redirect_to_chain(response, location, context)
    process_redirect_location(location, context)


def create_response_handler(context: RedirectContext) -> Callable[[Response], None]:
    """Create a response handler for the given context."""
    return lambda response: handle_redirect_response(response, context)


def should_continue_request(context: RedirectContext, request_url: str) -> bool:
    """Check if request should continue."""
    return not (context.external_redirect and request_url.startswith("http"))


def should_abort_request(context: RedirectContext, request_url: str) -> bool:
    """Check if request should be aborted."""
    return (
        context.external_redirect
        and request_url.startswith("http")
        and not is_internal_domain(request_url)
    )


async def handle_external_request(route: Route, context: RedirectContext) -> None:
    """Handle external requests during navigation."""
    request_url = route.request.url

    if should_continue_request(context, request_url):
        await route.continue_()
        return

    if should_abort_request(context, request_url):
        context.aborted = True
        await route.abort()
        return

    await route.continue_()


def create_request_handler(
    context: RedirectContext,
) -> Callable[[Route], Awaitable[None]]:
    """Create a request handler for the given context."""

    async def handler(route: Route) -> None:
        await handle_external_request(route, context)

    return handler


async def setup_page_handlers(
    page: Page, context: RedirectContext
) -> Callable[[], Awaitable[None]]:
    """Setup page handlers and return cleanup function."""
    response_handler = create_response_handler(context)
    request_handler = create_request_handler(context)

    page.on("response", response_handler)
    await page.route("**/*", request_handler)

    async def cleanup():
        page.remove_listener("response", response_handler)
        await page.unroute("**/*", request_handler)

    return cleanup


async def wait_for_page_load(page: Page, context: RedirectContext) -> None:
    """Wait for page to load with appropriate timeout."""
    await page.wait_for_timeout(1000)

    if context.external_redirect:
        log_message("   🌐 External redirect detected, skipping full load")
        return

    log_message("   ⏳ Waiting for page load...")
    try:
        await page.wait_for_load_state("networkidle", timeout=10000)
    except Exception:
        log_message("   ⚠️  Page load timeout (continuing)")


def log_navigation_result(page: Page, context: RedirectContext) -> str:
    """Log navigation result and return final URL."""
    if context.aborted:
        log_message("   ⚡ Navigation aborted to prevent hanging")

    final_url = page.url
    log_message(f"   ✅ Final URL: {final_url}")

    if context.redirect_chain:
        log_message(f"   📍 {len(context.redirect_chain)} redirect(s) detected")

    return final_url


def detect_javascript_interference(
    original_href: str, final_url: str, context: RedirectContext
) -> bool:
    """Detect if JavaScript interfered with navigation."""
    return (
        original_href != final_url
        and len(context.redirect_chain) == 0
        and not context.external_redirect
    )


def create_success_result(
    link_index: int, original_href: str, final_url: str, context: RedirectContext
) -> LinkTestResult:
    """Create a successful test result."""
    return LinkTestResult(
        link_index=link_index,
        success=True,
        original_href=original_href,
        final_url=final_url,
        redirect_chain=context.redirect_chain.copy(),
        external_redirect=context.external_redirect,
        aborted=context.aborted,
        javascript_interference=detect_javascript_interference(
            original_href, final_url, context
        ),
    )


def create_error_result(
    link_index: int, error: str, context: RedirectContext
) -> LinkTestResult:
    """Create an error test result."""
    return LinkTestResult(
        link_index=link_index,
        success=False,
        external_redirect=context.external_redirect,
        aborted=context.aborted,
        error=error,
    )


async def navigate_to_base_url(page: Page, base_url: str, link_index: int) -> None:
    """Navigate back to base URL if needed."""
    if link_index > 0:
        log_message(f"   📍 Navigating back to {base_url}...")
        await page.goto(base_url)
        await page.wait_for_load_state("networkidle")


async def get_current_link(
    page: Page, link_selector: str, original_index: int
) -> Optional[ElementHandle]:
    """Get the current link element by index."""
    current_links = await page.query_selector_all(link_selector)
    if original_index < len(current_links):
        return current_links[original_index]
    return None


async def process_link_click(
    page: Page, current_link: ElementHandle, context: RedirectContext
) -> Tuple[str, str]:
    """Process clicking a link and return original href and final URL."""
    original_href = await current_link.get_attribute("href") or ""

    log_message("   🖱️  Clicking link...")
    await current_link.click()

    await wait_for_page_load(page, context)
    final_url = log_navigation_result(page, context)

    return original_href, final_url


async def test_single_link(
    page: Page,
    filtered_link: FilteredLink,
    link_index: int,
    link_selector: str,
    base_url: str,
) -> LinkTestResult:
    """Test a single link."""
    original_index = filtered_link.index
    expected_href = filtered_link.href

    log_message(f"\n🔗 Testing link {link_index + 1}: {expected_href}")

    await navigate_to_base_url(page, base_url, link_index)

    current_link = await get_current_link(page, link_selector, original_index)
    if not current_link:
        return create_error_result(
            original_index,
            f"Link {original_index} not found after navigation",
            create_redirect_context(),
        )

    context = create_redirect_context()
    cleanup = await setup_page_handlers(page, context)

    try:
        original_href, final_url = await process_link_click(page, current_link, context)
        return create_success_result(original_index, original_href, final_url, context)
    except Exception as e:
        error_msg = str(e)
        log_message(f"   ❌ Error: {error_msg}")
        return create_error_result(original_index, error_msg, context)
    finally:
        await cleanup()


async def test_all_links(
    page: Page, filtered_links: List["FilteredLink"], link_selector: str, base_url: str
) -> List["LinkTestResult"]:
    """Test all filtered links."""
    results: List[LinkTestResult] = []

    for i, filtered_link in enumerate(filtered_links):
        if not filtered_link:
            continue

        result = await test_single_link(page, filtered_link, i, link_selector, base_url)
        results.append(result)

    return results


def calculate_summary(results: List["LinkTestResult"]) -> "TestSummary":
    """Calculate summary statistics from results."""
    return TestSummary(
        successful=len([r for r in results if r.success]),
        failed=len([r for r in results if not r.success]),
        external_redirects=len([r for r in results if r.external_redirect]),
        javascript_interference=len([r for r in results if r.javascript_interference]),
    )


async def verify_email_link_content(
    email_element: ElementHandle,
) -> Dict[str, str | None]:
    """Verify email link content."""
    email_text = await email_element.text_content()
    email_href = await email_element.get_attribute("href")

    valid = bool(
        email_text
        and "dave@dave.io" in email_text
        and email_href
        and "mailto:dave@dave.io" in email_href
    )
    return {
        "valid": "true" if valid else "false",
        "text": email_text,
        "href": email_href,
    }


def has_timed_out(start_time: float, max_wait_time: int) -> bool:
    """Check if operation has timed out."""
    return (time.time() * 1000) - start_time >= max_wait_time


def create_timeout_result() -> EmailTestResult:
    """Create timeout result for email test."""
    log_message("   ❌ Email link 'a.email-link' not found after 3000ms")
    return EmailTestResult(
        success=False, error="Email link 'a.email-link' not found after 3000ms"
    )


async def check_email_link_once(
    page: Page, start_time: float
) -> Optional[EmailTestResult]:
    """Check for email link once."""
    email_element = page.locator("a.email-link").first
    email_exists = await email_element.count() > 0

    if not email_exists:
        return None

    elapsed_time = int((time.time() * 1000) - start_time)
    element_handle = await email_element.element_handle()
    if not element_handle:
        return None
    result = await verify_email_link_content(element_handle)

    if result["valid"] == "true":
        log_message(f"   ✅ Email link found and verified in {elapsed_time}ms")
        return EmailTestResult(
            success=True, final_text="dave@dave.io", replacement_time=elapsed_time
        )

    log_message(
        f'   ❌ Email link found but content incorrect: text="{result["text"]}", href="{result["href"]}"'
    )
    return EmailTestResult(
        success=False,
        error=f'Email link found but content incorrect: text="{result["text"]}", href="{result["href"]}"',
    )


async def wait_for_and_check_email_link(
    page: Page, start_time: float
) -> EmailTestResult:
    """Wait for and check email link."""
    log_message("   ⏳ Checking for email link (polling every 200ms, max 3000ms)...")

    max_wait_time = 3000
    poll_interval = 200

    while not has_timed_out(start_time, max_wait_time):
        result = await check_email_link_once(page, start_time)
        if result:
            return result
        await page.wait_for_timeout(poll_interval)

    return create_timeout_result()


async def test_email_decoding(page: Page) -> EmailTestResult:
    """Test email decoding functionality."""
    log_message("\n📧 Testing email decoding...")

    try:
        start_time = time.time() * 1000
        return await wait_for_and_check_email_link(page, start_time)
    except Exception as e:
        error_msg = str(e)
        log_message(f"   ❌ Email test error: {error_msg}")
        return EmailTestResult(success=False, error=error_msg)


def create_error_result_main(error: str) -> TestResults:
    """Create main error result."""
    return TestResults(
        success=False,
        total_links=0,
        results=[],
        email_test=EmailTestResult(
            success=False, error="Test suite failed before email test could run"
        ),
        summary=TestSummary(
            successful=0, failed=0, external_redirects=0, javascript_interference=0
        ),
        error=error,
    )


async def test_link_redirects(url: str, link_selector: str) -> TestResults:
    """Main function to test link redirects."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(url)

            # Test email decoding first
            email_test = await test_email_decoding(page)

            all_links = await find_all_links(page, link_selector)
            filtered_links = await filter_go_links(all_links, url)

            if not filtered_links:
                return TestResults(
                    success=False,
                    total_links=0,
                    results=[],
                    email_test=email_test,
                    summary=TestSummary(
                        successful=0,
                        failed=0,
                        external_redirects=0,
                        javascript_interference=0,
                    ),
                    error=f"Found {len(all_links)} links matching selector, but none point to https://dave.io/go/*",
                )

            log_message(
                f"🔍 Found {len(filtered_links)} links pointing to https://dave.io/go/* to test"
            )

            results = await test_all_links(page, filtered_links, link_selector, url)
            summary = calculate_summary(results)

            return TestResults(
                success=True,
                total_links=len(filtered_links),
                results=results,
                email_test=email_test,
                summary=summary,
            )
        except Exception as e:
            return create_error_result_main(str(e))
        finally:
            await browser.close()


def serialize_result(obj: Any) -> Any:
    """Custom serializer for dataclasses."""
    return asdict(obj) if hasattr(obj, "__dataclass_fields__") else obj


async def run_tests() -> TestResults:
    """Run the actual tests and return results."""
    return await test_link_redirects("https://dave.io", "a.link-url")


def output_results(result: TestResults) -> int:
    """Output test results to stderr (if verbose) and stdout. Return exit code."""

    log_message(
        f"\n📊 Test completed! Tested {result.total_links} links pointing to https://dave.io/go/*"
    )

    # Report email test results
    log_message("\n📧 Email decoding test:")
    if result.email_test.success:
        log_message(
            f"   ✅ Email decoded successfully in {result.email_test.replacement_time}ms"
        )
        log_message(f"   📝 Email link verified: '{result.email_test.final_text}'")
    else:
        log_message(f"   ❌ Email test failed: {result.email_test.error}")

    # Report link test results
    if result.success:
        log_message("\n🔗 Link test results:")
        log_message(f"   ✅ {result.summary.successful} successful")
        log_message(f"   ❌ {result.summary.failed} failed")
        log_message(f"   🌐 {result.summary.external_redirects} external redirects")
        log_message(
            f"   ⚠️  {result.summary.javascript_interference} JavaScript interference"
        )
    else:
        log_message(f"   ❌ Test suite failed: {result.error}")

    log_message("\n📝 Full JSON report written to STDOUT")

    # Output only JSON to STDOUT
    # Convert dataclasses to dict for JSON serialization
    result_dict = asdict(result)
    print(json.dumps(result_dict, indent=2))

    # Exit with appropriate code based on test results
    has_failures = (
        not result.success or not result.email_test.success or result.summary.failed > 0
    )
    return 1 if has_failures else 0


@click.command()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output to stderr")
@click.option("--force-fail", is_flag=True, help="Skip tests and exit with code 1")
@click.option("--force-pass", is_flag=True, help="Skip tests and exit with code 0")
def main(verbose: bool, force_fail: bool, force_pass: bool) -> None:
    """Monitor script to test link redirects and email decoding on dave.io."""
    global _verbose
    _verbose = verbose

    # Handle force flags first
    if force_fail and force_pass:
        click.echo("Error: Cannot specify both --force-fail and --force-pass", err=True)
        sys.exit(1)
    elif force_fail:
        log_message("🚫 Force fail mode - skipping tests")
        error_result = create_error_result_main("Force fail mode enabled")
        print(json.dumps(asdict(error_result), indent=2))
        sys.exit(1)
    elif force_pass:
        log_message("✅ Force pass mode - skipping tests")
        success_result = TestResults(
            success=True,
            total_links=0,
            results=[],
            email_test=EmailTestResult(
                success=True, final_text="dave@dave.io", replacement_time=0
            ),
            summary=TestSummary(
                successful=0, failed=0, external_redirects=0, javascript_interference=0
            ),
        )
        print(json.dumps(asdict(success_result), indent=2))
        sys.exit(0)

    # Run actual tests
    try:
        result = asyncio.run(run_tests())
        exit_code = output_results(result)
        sys.exit(exit_code)
    except Exception as e:
        log_message(f"❌ Fatal error: {str(e)}")

        # Output error as JSON to STDOUT
        error_result = create_error_result_main(str(e))
        print(json.dumps(asdict(error_result), indent=2))

        sys.exit(1)


if __name__ == "__main__":
    main()
