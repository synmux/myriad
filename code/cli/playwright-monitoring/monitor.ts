import { chromium } from "playwright"
import type { Browser, BrowserContext, Page, Response, Route } from "playwright"
import { promises as fs } from "fs"

interface LinkTestResult {
    linkIndex: number;
    success: boolean;
    originalHref?: string;
    finalUrl?: string;
    redirectChain?: { from: string; to: string; status: number }[];
    javascriptInterference?: boolean;
    externalRedirect?: boolean;
    aborted?: boolean;
    error?: string;
}

interface TestResults {
    success: boolean;
    totalLinks: number;
    results: LinkTestResult[];
    summary: {
        successful: number;
        failed: number;
        externalRedirects: number;
        javascriptInterference: number;
    };
    error?: string;
}

async function testLinkRedirects(url: string, linkSelector: string): Promise<TestResults> {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    const page = await context.newPage();

    try {
        await page.goto(url);

        // Find all links matching the selector
        const allLinks = await page.$$(linkSelector);
        if (allLinks.length === 0) {
            return {
                success: false,
                totalLinks: 0,
                results: [],
                summary: {
                    successful: 0,
                    failed: 0,
                    externalRedirects: 0,
                    javascriptInterference: 0
                },
                error: `No links found matching selector: ${linkSelector}`
            };
        }

        // Filter links to only include those pointing to https://dave.io/go/*
        const filteredLinks: { element: any, index: number, href: string }[] = [];
        for (let i = 0; i < allLinks.length; i++) {
            const href = await allLinks[i]?.getAttribute('href');
            if (href) {
                // Handle both absolute and relative URLs
                const absoluteHref = href.startsWith('http') ? href : new URL(href, url).href;
                if (absoluteHref.startsWith('https://dave.io/go/')) {
                    filteredLinks.push({ element: allLinks[i], index: i, href: absoluteHref });
                }
            }
        }

        if (filteredLinks.length === 0) {
            return {
                success: false,
                totalLinks: allLinks.length,
                results: [],
                summary: {
                    successful: 0,
                    failed: 0,
                    externalRedirects: 0,
                    javascriptInterference: 0
                },
                error: `Found ${allLinks.length} links matching selector, but none point to https://dave.io/go/*`
            };
        }

        console.error(`🔍 Found ${filteredLinks.length} links pointing to https://dave.io/go/* to test`);

        const results: LinkTestResult[] = [];

        for (let i = 0; i < filteredLinks.length; i++) {
            const filteredLink = filteredLinks[i];
            if (!filteredLink) continue;

            const { element: linkElement, index: originalIndex, href: expectedHref } = filteredLink;

            console.error(`\n🔗 Testing link ${i + 1}/${filteredLinks.length}: ${expectedHref}`);

            // Navigate back to original page for each test (except the first)
            if (i > 0) {
                console.error(`   📍 Navigating back to ${url}...`);
                await page.goto(url);
                await page.waitForLoadState('networkidle');
            }

            // Re-find the links since we navigated back
            const currentLinks = await page.$$(linkSelector);
            const currentLink = currentLinks[originalIndex];

            if (!currentLink) {
                results.push({
                    linkIndex: originalIndex,
                    success: false,
                    error: `Link ${originalIndex} not found after navigation`
                });
                continue;
            }

                        // Track redirects for this specific link test
            const redirectChain: { from: string; to: string; status: number }[] = [];
            let externalRedirect = false;
            let aborted = false;

            const responseHandler = (response: Response) => {
                if (response.status() >= 300 && response.status() < 400) {
                    const location = response.headers()['location'] ?? '';
                    redirectChain.push({
                        from: response.url(),
                        to: location,
                        status: response.status()
                    });

                    // Check if redirect is taking us outside dave.io (strict domain check)
                    if (location && (location.startsWith('http') || location.startsWith('//'))) {
                        const redirectUrl = location.startsWith('//') ? `https:${location}` : location;
                        try {
                            const redirectDomain = new URL(redirectUrl).hostname;
                            // Only https://dave.io is considered internal, not subdomains
                            if (redirectDomain !== 'dave.io') {
                                externalRedirect = true;
                            }
                        } catch {
                            // If URL parsing fails, treat as external
                            externalRedirect = true;
                        }
                    }
                }
            };

            // Abort navigation if we detect external redirect
            const requestHandler = async (route: Route) => {
                const requestUrl = route.request().url();

                // If this request is outside dave.io and we already detected external redirect, abort
                if (externalRedirect && requestUrl.startsWith('http')) {
                    try {
                        const requestDomain = new URL(requestUrl).hostname;
                        // Only https://dave.io is considered internal, not subdomains
                        if (requestDomain !== 'dave.io') {
                            aborted = true;
                            await route.abort();
                            return;
                        }
                    } catch {
                        // If URL parsing fails, treat as external and abort
                        aborted = true;
                        await route.abort();
                        return;
                    }
                }

                await route.continue();
            };

            page.on('response', responseHandler);
            await page.route('**/*', requestHandler);

            try {
                // Get the href before clicking
                const originalHref = await currentLink.getAttribute('href') ?? undefined;

                console.error(`   🖱️  Clicking link...`);
                // Click and wait for navigation, but with timeout and early abort
                await currentLink.click();

                // Wait briefly for initial navigation/redirects to be detected
                await page.waitForTimeout(1000);

                // If we detected external redirect, don't wait for full load
                if (!externalRedirect) {
                    console.error(`   ⏳ Waiting for page load...`);
                    try {
                        await page.waitForLoadState('networkidle', { timeout: 10000 });
                    } catch (e) {
                        // Timeout is ok if we got the redirect info we needed
                        console.error(`   ⚠️  Page load timeout (continuing)`);
                    }
                } else {
                    console.error(`   🌐 External redirect detected, skipping full load`);
                }

                if (aborted) {
                    console.error(`   ⚡ Navigation aborted to prevent hanging`);
                }

                const finalUrl = page.url();
                console.error(`   ✅ Final URL: ${finalUrl}`);

                if (redirectChain.length > 0) {
                    console.error(`   📍 ${redirectChain.length} redirect(s) detected`);
                }

                results.push({
                    linkIndex: originalIndex,
                    success: true,
                    originalHref,
                    finalUrl,
                    redirectChain: [...redirectChain],
                    externalRedirect,
                    aborted,
                    javascriptInterference: originalHref !== finalUrl && redirectChain.length === 0 && !externalRedirect
                });
            } catch (error: unknown) {
                const errorMsg = error instanceof Error ? error.message : String(error);
                console.error(`   ❌ Error: ${errorMsg}`);

                results.push({
                    linkIndex: originalIndex,
                    success: false,
                    externalRedirect,
                    aborted,
                    error: errorMsg
                });
            } finally {
                // Remove the event listeners to prevent accumulation
                page.off('response', responseHandler);
                await page.unroute('**/*', requestHandler);
            }
        }

        // Calculate summary statistics
        const successCount = results.filter(r => r.success).length;
        const failureCount = results.filter(r => !r.success).length;
        const externalRedirectCount = results.filter(r => r.externalRedirect).length;
        const javascriptInterferenceCount = results.filter(r => r.javascriptInterference).length;

        return {
            success: true,
            totalLinks: filteredLinks.length,
            results,
            summary: {
                successful: successCount,
                failed: failureCount,
                externalRedirects: externalRedirectCount,
                javascriptInterference: javascriptInterferenceCount
            }
        };

    } catch (error: unknown) {
        return {
            success: false,
            totalLinks: 0,
            results: [],
            summary: {
                successful: 0,
                failed: 0,
                externalRedirects: 0,
                javascriptInterference: 0
            },
            error: error instanceof Error ? error.message : String(error)
        };
    } finally {
        await browser.close();
    }
}

// Example usage
testLinkRedirects('https://dave.io', 'a.link-url')
    .then(result => {
        console.error(`\n📊 Test completed! Tested ${result.totalLinks} links pointing to https://dave.io/go/*`);

                if (result.success) {
            console.error(`   ✅ ${result.summary.successful} successful`);
            console.error(`   ❌ ${result.summary.failed} failed`);
            console.error(`   🌐 ${result.summary.externalRedirects} external redirects`);
            console.error(`   ⚠️  ${result.summary.javascriptInterference} JavaScript interference`);
        } else {
            console.error(`   ❌ Test suite failed: ${result.error}`);
        }

        console.error(`\n📝 Full JSON report written to STDOUT`);

        // Output only JSON to STDOUT
        console.log(JSON.stringify(result, null, 2));
    })
    .catch(error => {
        console.error(`❌ Fatal error: ${error instanceof Error ? error.message : String(error)}`);

        // Output error as JSON to STDOUT
        console.log(JSON.stringify({
            success: false,
            totalLinks: 0,
            results: [],
            summary: {
                successful: 0,
                failed: 0,
                externalRedirects: 0,
                javascriptInterference: 0
            },
            error: error instanceof Error ? error.message : String(error)
        }, null, 2));

        process.exit(1);
    });
