import type { ElementHandle, Page, Response, Route } from "playwright"
import { chromium } from "playwright"

interface LinkTestResult {
  linkIndex: number
  success: boolean
  originalHref?: string
  finalUrl?: string
  redirectChain?: { from: string; to: string; status: number }[]
  javascriptInterference?: boolean
  externalRedirect?: boolean
  aborted?: boolean
  error?: string
}

interface TestResults {
  success: boolean
  totalLinks: number
  results: LinkTestResult[]
  summary: {
    successful: number
    failed: number
    externalRedirects: number
    javascriptInterference: number
  }
  error?: string
}

interface FilteredLink {
  element: ElementHandle<HTMLAnchorElement>
  index: number
  href: string
}

interface RedirectContext {
  redirectChain: { from: string; to: string; status: number }[]
  externalRedirect: boolean
  aborted: boolean
}

// Helper function to check if domain is internal (only dave.io)
function isInternalDomain(url: string): boolean {
  try {
    const domain = new URL(url).hostname
    return domain === "dave.io"
  } catch {
    return false
  }
}

// Helper function to normalize URL
function normalizeUrl(href: string, baseUrl: string): string {
  return href.startsWith("http") ? href : new URL(href, baseUrl).href
}

// Helper function to check if URL points to go links
function isGoLink(url: string): boolean {
  return url.startsWith("https://dave.io/go/")
}

async function findAllLinks(page: Page, linkSelector: string): Promise<ElementHandle<HTMLAnchorElement>[]> {
  const allLinks = await page.$$(linkSelector)
  if (allLinks.length === 0) {
    throw new Error(`No links found matching selector: ${linkSelector}`)
  }
  return allLinks as ElementHandle<HTMLAnchorElement>[]
}

async function processLinkElement(
  element: ElementHandle<HTMLAnchorElement>,
  index: number,
  baseUrl: string
): Promise<FilteredLink | null> {
  const href = await element.getAttribute("href")
  if (!href) {
    return null
  }

  const absoluteHref = normalizeUrl(href, baseUrl)
  if (!isGoLink(absoluteHref)) {
    return null
  }

  return {
    element,
    index,
    href: absoluteHref
  }
}

async function filterGoLinks(allLinks: ElementHandle<HTMLAnchorElement>[], baseUrl: string): Promise<FilteredLink[]> {
  const filteredLinks: FilteredLink[] = []

  for (let i = 0; i < allLinks.length; i++) {
    const element = allLinks[i]
    if (!element) {
      continue
    }

    const processedLink = await processLinkElement(element, i, baseUrl)
    if (processedLink) {
      filteredLinks.push(processedLink)
    }
  }

  return filteredLinks
}

function createRedirectContext(): RedirectContext {
  return {
    redirectChain: [],
    externalRedirect: false,
    aborted: false
  }
}

function isRedirectResponse(status: number): boolean {
  return status >= 300 && status < 400
}

function addRedirectToChain(response: Response, location: string, context: RedirectContext): void {
  context.redirectChain.push({
    from: response.url(),
    to: location,
    status: response.status()
  })
}

function processRedirectLocation(location: string, context: RedirectContext): void {
  if (!(location && (location.startsWith("http") || location.startsWith("//")))) {
    return
  }

  const redirectUrl = location.startsWith("//") ? `https:${location}` : location
  if (!isInternalDomain(redirectUrl)) {
    context.externalRedirect = true
  }
}

function handleRedirectResponse(response: Response, context: RedirectContext): void {
  if (!isRedirectResponse(response.status())) {
    return
  }

  const location = response.headers().location ?? ""
  addRedirectToChain(response, location, context)
  processRedirectLocation(location, context)
}

function createResponseHandler(context: RedirectContext) {
  return (response: Response) => handleRedirectResponse(response, context)
}

function shouldContinueRequest(context: RedirectContext, requestUrl: string): boolean {
  return !(context.externalRedirect && requestUrl.startsWith("http"))
}

function shouldAbortRequest(context: RedirectContext, requestUrl: string): boolean {
  return context.externalRedirect && requestUrl.startsWith("http") && !isInternalDomain(requestUrl)
}

async function handleExternalRequest(route: Route, context: RedirectContext): Promise<void> {
  const requestUrl = route.request().url()

  if (shouldContinueRequest(context, requestUrl)) {
    await route.continue()
    return
  }

  if (shouldAbortRequest(context, requestUrl)) {
    context.aborted = true
    await route.abort()
    return
  }

  await route.continue()
}

function createRequestHandler(context: RedirectContext) {
  return async (route: Route) => handleExternalRequest(route, context)
}

async function setupPageHandlers(page: Page, context: RedirectContext): Promise<() => Promise<void>> {
  const responseHandler = createResponseHandler(context)
  const requestHandler = createRequestHandler(context)

  page.on("response", responseHandler)
  await page.route("**/*", requestHandler)

  return async () => {
    page.off("response", responseHandler)
    await page.unroute("**/*", requestHandler)
  }
}

async function waitForPageLoad(page: Page, context: RedirectContext): Promise<void> {
  await page.waitForTimeout(1000)

  if (context.externalRedirect) {
    console.error("   🌐 External redirect detected, skipping full load")
    return
  }

  console.error("   ⏳ Waiting for page load...")
  try {
    await page.waitForLoadState("networkidle", { timeout: 10000 })
  } catch {
    console.error("   ⚠️  Page load timeout (continuing)")
  }
}

function logNavigationResult(page: Page, context: RedirectContext): string {
  if (context.aborted) {
    console.error("   ⚡ Navigation aborted to prevent hanging")
  }

  const finalUrl = page.url()
  console.error(`   ✅ Final URL: ${finalUrl}`)

  if (context.redirectChain.length > 0) {
    console.error(`   📍 ${context.redirectChain.length} redirect(s) detected`)
  }

  return finalUrl
}

function detectJavaScriptInterference(originalHref: string, finalUrl: string, context: RedirectContext): boolean {
  return originalHref !== finalUrl && context.redirectChain.length === 0 && !context.externalRedirect
}

function createSuccessResult(
  linkIndex: number,
  originalHref: string,
  finalUrl: string,
  context: RedirectContext
): LinkTestResult {
  return {
    linkIndex,
    success: true,
    originalHref,
    finalUrl,
    redirectChain: [...context.redirectChain],
    externalRedirect: context.externalRedirect,
    aborted: context.aborted,
    javascriptInterference: detectJavaScriptInterference(originalHref, finalUrl, context)
  }
}

function createErrorResult(linkIndex: number, error: string, context: RedirectContext): LinkTestResult {
  return {
    linkIndex,
    success: false,
    externalRedirect: context.externalRedirect,
    aborted: context.aborted,
    error
  }
}

async function navigateToBaseUrl(page: Page, baseUrl: string, linkIndex: number): Promise<void> {
  if (linkIndex > 0) {
    console.error(`   📍 Navigating back to ${baseUrl}...`)
    await page.goto(baseUrl)
    await page.waitForLoadState("networkidle")
  }
}

async function getCurrentLink(
  page: Page,
  linkSelector: string,
  originalIndex: number
): Promise<ElementHandle<HTMLAnchorElement> | null> {
  const currentLinks = await page.$$(linkSelector)
  return currentLinks[originalIndex] as ElementHandle<HTMLAnchorElement> | null
}

async function processLinkClick(
  page: Page,
  currentLink: ElementHandle<HTMLAnchorElement>,
  context: RedirectContext
): Promise<{ originalHref: string; finalUrl: string }> {
  const originalHref = (await currentLink.getAttribute("href")) ?? ""

  console.error("   🖱️  Clicking link...")
  await currentLink.click()

  await waitForPageLoad(page, context)
  const finalUrl = logNavigationResult(page, context)

  return { originalHref, finalUrl }
}

async function testSingleLink(
  page: Page,
  filteredLink: FilteredLink,
  linkIndex: number,
  linkSelector: string,
  baseUrl: string
): Promise<LinkTestResult> {
  const { index: originalIndex, href: expectedHref } = filteredLink

  console.error(`\n🔗 Testing link ${linkIndex + 1}: ${expectedHref}`)

  await navigateToBaseUrl(page, baseUrl, linkIndex)

  const currentLink = await getCurrentLink(page, linkSelector, originalIndex)
  if (!currentLink) {
    return createErrorResult(originalIndex, `Link ${originalIndex} not found after navigation`, createRedirectContext())
  }

  const context = createRedirectContext()
  const cleanup = await setupPageHandlers(page, context)

  try {
    const { originalHref, finalUrl } = await processLinkClick(page, currentLink, context)
    return createSuccessResult(originalIndex, originalHref, finalUrl, context)
  } catch (error: unknown) {
    const errorMsg = error instanceof Error ? error.message : String(error)
    console.error(`   ❌ Error: ${errorMsg}`)
    return createErrorResult(originalIndex, errorMsg, context)
  } finally {
    await cleanup()
  }
}

async function testAllLinks(
  page: Page,
  filteredLinks: FilteredLink[],
  linkSelector: string,
  baseUrl: string
): Promise<LinkTestResult[]> {
  const results: LinkTestResult[] = []

  for (let i = 0; i < filteredLinks.length; i++) {
    const filteredLink = filteredLinks[i]
    if (!filteredLink) {
      continue
    }

    const result = await testSingleLink(page, filteredLink, i, linkSelector, baseUrl)
    results.push(result)
  }

  return results
}

function calculateSummary(results: LinkTestResult[]) {
  return {
    successful: results.filter((r) => r.success).length,
    failed: results.filter((r) => !r.success).length,
    externalRedirects: results.filter((r) => r.externalRedirect).length,
    javascriptInterference: results.filter((r) => r.javascriptInterference).length
  }
}

function createErrorResult_Main(error: string): TestResults {
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
    error
  }
}

async function testLinkRedirects(url: string, linkSelector: string): Promise<TestResults> {
  const browser = await chromium.launch({ headless: true })
  const context = await browser.newContext()
  const page = await context.newPage()

  try {
    await page.goto(url)

    const allLinks = await findAllLinks(page, linkSelector)
    const filteredLinks = await filterGoLinks(allLinks, url)

    if (filteredLinks.length === 0) {
      return createErrorResult_Main(
        `Found ${allLinks.length} links matching selector, but none point to https://dave.io/go/*`
      )
    }

    console.error(`🔍 Found ${filteredLinks.length} links pointing to https://dave.io/go/* to test`)

    const results = await testAllLinks(page, filteredLinks, linkSelector, url)
    const summary = calculateSummary(results)

    return {
      success: true,
      totalLinks: filteredLinks.length,
      results,
      summary
    }
  } catch (error: unknown) {
    return createErrorResult_Main(error instanceof Error ? error.message : String(error))
  } finally {
    await browser.close()
  }
}

// Example usage
testLinkRedirects("https://dave.io", "a.link-url")
  .then((result) => {
    console.error(`\n📊 Test completed! Tested ${result.totalLinks} links pointing to https://dave.io/go/*`)

    if (result.success) {
      console.error(`   ✅ ${result.summary.successful} successful`)
      console.error(`   ❌ ${result.summary.failed} failed`)
      console.error(`   🌐 ${result.summary.externalRedirects} external redirects`)
      console.error(`   ⚠️  ${result.summary.javascriptInterference} JavaScript interference`)
    } else {
      console.error(`   ❌ Test suite failed: ${result.error}`)
    }

    console.error("\n📝 Full JSON report written to STDOUT")

    // Output only JSON to STDOUT
    console.log(JSON.stringify(result, null, 2))
  })
  .catch((error) => {
    console.error(`❌ Fatal error: ${error instanceof Error ? error.message : String(error)}`)

    // Output error as JSON to STDOUT
    console.log(
      JSON.stringify(
        {
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
        },
        null,
        2
      )
    )

    process.exit(1)
  })
