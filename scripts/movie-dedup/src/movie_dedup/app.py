"""FastAPI application — routes + HTMX fragments."""

from __future__ import annotations

import asyncio
from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .config import LIBRARY_ROOT
from .deleter import execute, preview
from .scanner import iter_flagged_dirs
from .state import STORE, flagged_to_view

PACKAGE_DIR = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(PACKAGE_DIR / "templates"))
STATIC_DIR = PACKAGE_DIR / "static"

app = FastAPI(title="movie-dedup")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def _human_bytes(n: int) -> str:
    step = 1024.0
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(n) < step:
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} B"
        n = int(n / step)
    return f"{n} PB"


TEMPLATES.env.filters["human_bytes"] = _human_bytes


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return TEMPLATES.TemplateResponse(  # type: ignore[return-value]
        request,
        "index.html",
        {"scan": STORE.current(), "library_root": str(LIBRARY_ROOT)},
    )


async def _run_scan(scan_id: str) -> None:
    """Background task: walk the library and stream flagged dirs into the store."""
    scanned = 0
    subdirs = sorted(
        p for p in LIBRARY_ROOT.iterdir() if p.is_dir() and not p.name.startswith(".")
    )
    total = len(subdirs)
    STORE.update_progress(scan_id, scanned=0, total=total)

    async for fd in iter_flagged_dirs(LIBRARY_ROOT):
        STORE.add_directory(scan_id, flagged_to_view(fd))
        scanned = max(scanned, 1)

    # Re-count progress by matching subdir names — iter_flagged_dirs doesn't emit skipped dirs.
    STORE.update_progress(scan_id, scanned=total, total=total)
    STORE.finish(scan_id)


@app.post("/scan")
async def start_scan() -> RedirectResponse:
    if not LIBRARY_ROOT.exists():
        raise HTTPException(
            status_code=400, detail=f"Library root not found: {LIBRARY_ROOT}"
        )
    scan = STORE.new_scan(LIBRARY_ROOT)
    asyncio.create_task(_run_scan(scan.scan_id))
    return RedirectResponse("/results", status_code=303)


@app.get("/results", response_class=HTMLResponse)
async def results(request: Request) -> HTMLResponse:
    scan = STORE.current()
    if scan is None:
        return RedirectResponse("/", status_code=303)  # type: ignore[return-value]
    return TEMPLATES.TemplateResponse(  # type: ignore[return-value]
        request,
        "results.html",
        {"scan": scan},
    )


@app.get("/scan/progress", response_class=HTMLResponse)
async def scan_progress(request: Request) -> HTMLResponse:
    """HTMX polls this fragment while a scan is running. When the scan has
    just finished, we return the 'done' fragment AND an HX-Refresh header so
    the browser reloads /results and sees the full flagged-dirs list."""
    scan = STORE.current()
    response = TEMPLATES.TemplateResponse(  # type: ignore[assignment]
        request,
        "_progress.html",
        {"scan": scan},
    )
    if scan is not None and not scan.running:
        response.headers["HX-Refresh"] = "true"
    return response


@app.post("/toggle", response_class=HTMLResponse)
async def toggle(
    request: Request,
    directory: str = Form(...),
    video_path: str = Form(...),
    remove: str = Form("off"),
) -> HTMLResponse:
    remove_bool = remove.lower() in {"on", "true", "1", "yes"}
    if not STORE.set_removal(directory, video_path, remove_bool):
        raise HTTPException(status_code=404, detail="copy not found")
    scan = STORE.current()
    return TEMPLATES.TemplateResponse(  # type: ignore[return-value]
        request,
        "_progress.html",
        {"scan": scan},
    )


@app.post("/clear")
async def clear_selection() -> RedirectResponse:
    STORE.apply_defaults(select=False)
    return RedirectResponse("/results", status_code=303)


@app.post("/preview", response_class=HTMLResponse)
async def preview_deletions(request: Request) -> HTMLResponse:
    scan = STORE.current()
    if scan is None:
        return RedirectResponse("/", status_code=303)  # type: ignore[return-value]

    target_paths: list[Path] = []
    per_directory: list[dict] = []
    for d in scan.directories:
        selected = [c for c in d.copies if c.remove]
        if not selected:
            continue
        files_for_dir: list[dict] = []
        subtotal = 0
        for c in selected:
            files_for_dir.append({"path": c.video_path, "size": c.size})
            target_paths.append(Path(c.video_path))
            subtotal += c.size
            for comp in c.companions:
                try:
                    size = Path(comp).stat().st_size
                except OSError:
                    size = 0
                files_for_dir.append({"path": comp, "size": size})
                target_paths.append(Path(comp))
                subtotal += size
        per_directory.append(
            {
                "name": d.name,
                "directory": d.directory,
                "files": files_for_dir,
                "subtotal": subtotal,
            }
        )

    batch = preview(target_paths)
    # Stash the batch under the current scan for the /delete endpoint.
    app.state.pending_batch = batch

    return TEMPLATES.TemplateResponse(  # type: ignore[return-value]
        request,
        "preview.html",
        {
            "per_directory": per_directory,
            "grand_total": batch.total_bytes,
            "count": len(batch.deletions),
        },
    )


@app.post("/delete", response_class=HTMLResponse)
async def delete(request: Request) -> HTMLResponse:
    batch = getattr(app.state, "pending_batch", None)
    if batch is None:
        return RedirectResponse("/results", status_code=303)  # type: ignore[return-value]
    result = execute(batch)
    app.state.pending_batch = None
    counts = {
        "deleted": sum(1 for d in result.deletions if d.outcome == "deleted"),
        "skipped": sum(1 for d in result.deletions if d.outcome == "skipped"),
        "error": sum(1 for d in result.deletions if d.outcome == "error"),
    }
    errors = [d for d in result.deletions if d.outcome in {"error", "skipped"}]
    return TEMPLATES.TemplateResponse(  # type: ignore[return-value]
        request,
        "done.html",
        {
            "counts": counts,
            "errors": errors,
            "total_bytes": sum(
                d.size for d in result.deletions if d.outcome == "deleted"
            ),
        },
    )


def main() -> None:
    import uvicorn

    from .config import HOST, PORT

    uvicorn.run("movie_dedup.app:app", host=HOST, port=PORT, reload=False)
