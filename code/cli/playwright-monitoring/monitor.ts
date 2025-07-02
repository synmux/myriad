import { chromium } from "playwright"
import type { Browser, BrowserContext, Page, Response } from "playwright"
import { promises as fs } from "fs"

interface MonitorConfig {
  headless?: boolean
  timeout?: number
  retries?: number
}

interface RedirectInfo {
  from: string
  status: number
}

interface RedirectTestResult {
  redirectCount: number
  redirects: RedirectInfo[]
}

interface JSContentTestResult {
  jsModified: Array<{
    selector: string
    hasEmail: boolean
  }>
}

interface PerformanceTestResult {
  domContentLoaded: number
  loadComplete: number
  totalTime: number
}

interface TestResult {
  error?: string
  success?: boolean
  redirectCount?: number
  redirects?: RedirectInfo[]
  jsModified?: Array<{
    selector: string
    hasEmail: boolean
  }>
  domContentLoaded?: number
  loadComplete?: number
  totalTime?: number
}

interface URLResult {
  url: string
  timestamp: string
  tests: Record<string, TestResult>
}

type TestFunction = (page: Page, url: string) => Promise<TestResult>

class WebsiteMonitor {
  private config: Required<MonitorConfig>
  private results: URLResult[]

  constructor(config: MonitorConfig = {}) {
    this.config = {
      headless: true,
      timeout: 30000,
      retries: 3,
      ...config
    }
    this.results = []
  }

  async runTests(urls: string[], tests: Record<string, TestFunction>): Promise<URLResult[]> {
    const browser: Browser = await chromium.launch({
      headless: this.config.headless
    })

    try {
      for (const url of urls) {
        const context: BrowserContext = await browser.newContext()
        const page: Page = await context.newPage()

        const urlResults: URLResult = {
          url,
          timestamp: new Date().toISOString(),
          tests: {}
        }

        for (const [testName, testFn] of Object.entries(tests)) {
          try {
            urlResults.tests[testName] = await testFn(page, url)
          } catch (error) {
            urlResults.tests[testName] = {
              error: error instanceof Error ? error.message : String(error),
              success: false
            }
          }
        }

        this.results.push(urlResults)
        await context.close()
      }
    } finally {
      await browser.close()
    }

    return this.results
  }

  async saveResults(filename: string): Promise<void> {
    await fs.writeFile(filename, JSON.stringify(this.results, null, 2))
  }
}

// Define monitoring tests
const monitoringTests: Record<string, TestFunction> = {
  async redirectTest(page: Page, url: string): Promise<RedirectTestResult> {
    const redirects: RedirectInfo[] = []
    page.on("response", (response: Response) => {
      if (response.status() >= 300 && response.status() < 400) {
        redirects.push({
          from: response.url(),
          status: response.status()
        })
      }
    })

    await page.goto(url)
    return { redirectCount: redirects.length, redirects }
  },

  async jsContentTest(page: Page, url: string): Promise<JSContentTestResult> {
    await page.goto(url, { waitUntil: "networkidle" })

    const jsModified = await page.evaluate(() => {
      const elements = document.querySelectorAll("[data-email], .email")
      return Array.from(elements).map((el) => ({
        selector: el.className || el.id,
        hasEmail: /[\w.-]+@[\w.-]+\.\w+/.test(el.textContent || "")
      }))
    })

    return { jsModified }
  },

  async performanceTest(page: Page, url: string): Promise<PerformanceTestResult> {
    await page.goto(url)

    return await page.evaluate(() => {
      const perf = performance.getEntriesByType("navigation")[0] as PerformanceNavigationTiming
      return {
        domContentLoaded: perf.domContentLoadedEventEnd - perf.domContentLoadedEventStart,
        loadComplete: perf.loadEventEnd - perf.loadEventStart,
        totalTime: perf.loadEventEnd - perf.fetchStart
      }
    })
  }
}

// Usage
const monitor = new WebsiteMonitor({ headless: true })
monitor.runTests(["https://dave.io"], monitoringTests).then((results) => {
  console.log("Monitoring complete:", results)
  return monitor.saveResults("monitoring-results.json")
})
