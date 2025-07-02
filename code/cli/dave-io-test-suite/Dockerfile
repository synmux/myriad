FROM oven/bun:1 AS base
WORKDIR /usr/src/app

# Install system dependencies required for Chromium with pinned versions
RUN apt-get update && apt-get install --no-install-recommends -y \
    # Core libraries
    libgtk-3-0=3.24.38-2~deb12u3 \
    libgbm1=22.3.6-1+deb12u1 \
    libnss3=2:3.87.1-1+deb12u1 \
    libxss1=1:1.2.3-1 \
    libasound2=1.2.8-1+b1 \
    # Fonts
    fonts-liberation=1:1.07.4-11 \
    fonts-noto-color-emoji=2.042-0+deb12u1 \
    # Additional dependencies
    libatk-bridge2.0-0=2.46.0-5 \
    libdrm2=2.4.114-1+b1 \
    libxcomposite1=1:0.4.5-1 \
    libxdamage1=1:1.1.6-1 \
    libxrandr2=2:1.5.2-2+b1 \
    libxkbcommon0=1.5.0-1 \
    ca-certificates=20230311+deb12u1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir -p /app && chown -R bun:bun /app

# Set environment variables for Playwright and install browsers as bun user
USER bun

ENV PLAYWRIGHT_BROWSERS_PATH=/app/playwright
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=0

WORKDIR /app

# Copy the monitoring script
COPY monitor.ts .

# Initialize a new Bun project and install Playwright
RUN bun init --yes && \
    bun add playwright && \
    bun install && \
    bun run playwright install chromium

# Add health check that verifies Chromium can launch
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD bun -e "import{chromium}from'playwright';(async()=>{const b=await chromium.launch({headless:true});await b.close()})().catch(()=>process.exit(1))"

# Run the monitoring script
ENTRYPOINT ["bun", "monitor.ts"]
