FROM ghcr.io/astral-sh/uv:0.7.19-python3.12-bookworm AS base

# OCI labels for proper container image metadata
LABEL org.opencontainers.image.description="Test suite for dave.io frontend"
LABEL org.opencontainers.image.source="https://github.com/daveio/myriad"
LABEL org.opencontainers.image.title="dave-io-test-suite"
LABEL org.opencontainers.image.licenses="MIT"

# No deps required due to `uv run playwright install-deps [...]`

# Create a non-root user for security
RUN groupadd --gid 1000 suite && \
    useradd --uid 1000 --gid suite --shell /bin/bash --create-home suite

# Set up working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock* /app/
COPY monitor.py /app/

# Install Python dependencies and the project
RUN uv run playwright install-deps chromium-headless-shell && \
    chown -R suite:suite /app

# Switch to non-root user
USER suite

RUN uv sync --frozen --no-cache && \
    uv run playwright install chromium-headless-shell

# # Set environment variables for Playwright to use system Chromium
# ENV PLAYWRIGHT_BROWSERS_PATH=0
# ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1

# Add health check that verifies Chromium can launch
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD uv run python -c "import asyncio; from playwright.async_api import async_playwright; \
    async def test(): \
        async with async_playwright() as p: \
            browser = await p.chromium.launch(headless=True, executable_path='/usr/bin/chromium'); \
            await browser.close(); \
    asyncio.run(test())"

# Run the monitoring script
ENTRYPOINT ["uv", "run", "python", "monitor.py"]
