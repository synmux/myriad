#!/usr/bin/env python3
from __future__ import annotations

import argparse
import logging
import re
from pathlib import Path

from playwright.sync_api import Error as PWError
from playwright.sync_api import TimeoutError as PWTimeoutError
from playwright.sync_api import sync_playwright

AUTOPAY_URL = "https://www.paypal.com/myaccount/autopay"  # entry point to automatic payments area. [web:74]

logger = logging.getLogger(__name__)


def ensure_dir(p: str) -> Path:
    d = Path(p)
    d.mkdir(parents=True, exist_ok=True)
    return d


def slug(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = s.strip("_")
    return s[:60] or "item"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--user-data-dir",
        required=True,
        help="Persistent Chromium profile dir (keeps you logged in).",
    )
    ap.add_argument("--headful", action="store_true", help="Show the browser window.")
    ap.add_argument(
        "--list-only",
        action="store_true",
        help="Only list merchant candidates; no cancelling.",
    )
    ap.add_argument(
        "--cancel-all",
        action="store_true",
        help="Attempt to cancel every automatic payment found.",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Proceed until confirm step, but do not confirm.",
    )
    ap.add_argument(
        "--dump-raw",
        action="store_true",
        help="On warnings/errors: save HTML + screenshot.",
    )
    ap.add_argument(
        "--artifact-dir",
        default="./artifacts",
        help="Where to write screenshots/HTML when --dump-raw.",
    )
    args = ap.parse_args()

    artifacts = ensure_dir(args.artifact_dir) if args.dump_raw else None

    with sync_playwright() as p:
        # launch_persistent_context keeps session state in user_data_dir. [web:97]
        context = p.chromium.launch_persistent_context(
            args.user_data_dir,
            headless=not args.headful,
            viewport={"width": 1400, "height": 900},
        )
        page = context.new_page()

        def capture(tag: str) -> None:
            if not artifacts:
                return
            page.screenshot(path=str(artifacts / f"{tag}.png"), full_page=True)
            (artifacts / f"{tag}.html").write_text(page.content(), encoding="utf-8")

        # Navigate to autopay page; if redirected to login, user logs in manually, then continue. [web:74]
        page.goto(AUTOPAY_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(1500)

        if "login" in page.url.lower():
            print(f"Redirected to login: {page.url}")
            print("Log in manually (including any 2FA), then press Enter here...")
            input()
            page.goto(AUTOPAY_URL, wait_until="domcontentloaded")
            page.wait_for_timeout(1500)

        print(f"Now at: {page.url}")

        # Best-effort confirmation we’re in the right place (text varies by locale). [web:74]
        try:
            page.get_by_text(re.compile(r"automatic payments", re.I)).first.wait_for(
                timeout=10_000
            )
        except PWTimeoutError:
            print(
                "Could not confirm 'Automatic payments' text; continuing best-effort."
            )
            capture("autopay_unconfirmed")

        # Heuristic: collect clickable merchant entries (UI changes often).
        candidates = []
        for loc in (page.get_by_role("link"), page.get_by_role("button")):
            for i in range(min(loc.count(), 400)):
                el = loc.nth(i)
                try:
                    txt = (el.inner_text(timeout=200) or "").strip()
                except (PWTimeoutError, PWError) as e:
                    logger.warning(
                        "Skipping candidate %s due to %s: %s",
                        i,
                        type(e).__name__,
                        e,
                    )
                    continue
                except Exception:
                    logger.exception(
                        "Unexpected error reading text for candidate %s", i
                    )
                    raise
                if not txt or len(txt) > 80:
                    continue
                if re.search(
                    r"(help|logout|log out|settings|wallet|summary)", txt, re.I
                ):
                    continue
                candidates.append((txt, el))

        # De-dupe by label
        seen = set()
        merchants = []
        for txt, el in candidates:
            if txt in seen:
                continue
            seen.add(txt)
            merchants.append((txt, el))

        print(f"Detected {len(merchants)} merchant candidates:")
        for txt, _ in merchants[:120]:
            print(f" - {txt}")

        if args.list_only:
            context.close()
            return 0

        if not args.cancel_all:
            print("Nothing cancelled (pass --cancel-all).")
            context.close()
            return 0

        if args.cancel_all and not args.dry_run:
            print("WARNING: You are about to cancel ALL autopay subscriptions!")
            try:
                confirm = input(
                    "Are you sure you want to cancel ALL autopay subscriptions? Type YES to confirm: "
                )
                if confirm.strip() != "YES":
                    print("Aborted.")
                    context.close()
                    return 0
            except KeyboardInterrupt:
                print("\nAborted.")
                context.close()
                return 0

        cancelled = 0
        for name, el in merchants:
            tag = slug(name)
            try:
                el.click(timeout=2500)
                page.wait_for_timeout(1200)

                # Try common action labels; exact text can vary. [web:74]
                action = None
                for pat in (
                    r"cancel",
                    r"stop paying",
                    r"remove paypal",
                    r"remove",
                    r"unlink",
                ):
                    loc = page.get_by_role("button", name=re.compile(pat, re.I))
                    if loc.count() > 0:
                        action = loc.first
                        break

                if not action:
                    print(f"[skip] {name}: no cancel/stop/remove/unlink button found")
                    continue

                action.click(timeout=2500)
                page.wait_for_timeout(800)

                if args.dry_run:
                    print(f"[dry-run] {name}: reached cancel flow; not confirming")
                    capture(f"dryrun_{tag}")
                    continue

                confirm = None
                for pat in (
                    r"confirm",
                    r"yes",
                    r"stop",
                    r"cancel automatic",
                    r"done",
                    r"remove",
                ):
                    loc = page.get_by_role("button", name=re.compile(pat, re.I))
                    if loc.count() > 0:
                        confirm = loc.first
                        break

                if not confirm:
                    print(
                        f"[warn] {name}: confirm button not found after opening cancel flow"
                    )
                    capture(f"no_confirm_{tag}")
                    continue

                confirm.click(timeout=2500)
                page.wait_for_timeout(1200)
                cancelled += 1
                print(f"[ok] cancelled: {name}")

            except Exception as e:
                print(f"[err] {name}: {e}")
                capture(f"err_{tag}")
                continue

        print(f"Cancelled: {cancelled}")
        context.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
