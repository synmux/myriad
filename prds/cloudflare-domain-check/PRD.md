---
title: Domain Availability Checker
type: task
status: draft
created: 2026-03-11
updated: 2026-03-11
version: 0.3
---

# Domain Availability Checker

**Type:** Task
**Created:** 2026-03-11
**Status:** Draft
**Author:** Dave
**Context File:** `.claude/prds/context/2026-03-11-domain-checker-task.json`

---

## 1. Overview

### Problem

Checking domain availability across hundreds of TLDs is a manual, tedious process. Existing tools either query WHOIS (slow, inconsistent, rate-limited per registrar) or rely on third-party aggregators that may not reflect Cloudflare Registrar pricing and availability. A developer wanting to find available domains for a brand name across all Cloudflare-supported TLDs has no efficient, scriptable way to do so.

### Solution

A CLI tool that accepts a domain name (e.g. `example`) and checks its availability across all 422 Cloudflare-supported TLDs using the Cloudflare Registrar API. Results are displayed in a formatted table showing availability status, registration eligibility, and pricing. Output can be piped as JSON for integration with other tools.

### Users

- **Primary:** Developers and system administrators who use Cloudflare Registrar and need to find available domains for projects, brands, or clients.
- **Secondary:** Domain investors and brand managers who want bulk availability checks scoped to Cloudflare's supported TLDs.

### Success Criteria

- Checks all 422 TLDs in a single invocation, completing within 120–150 seconds (requests are deliberately spread over a minimum of 120 seconds to stay within API rate limits)
- Correctly identifies available vs unavailable domains with zero false positives (matches Cloudflare dashboard results)
- Exits with code 0 on success, code 1 on fatal errors, and code 2 on partial failures (some TLDs failed)
- Produces parseable JSON output when `--json` flag is passed
- `--popular` completes in under 10 seconds (approximately 20 TLDs)
- `--short` completes in under 30 seconds (approximately 60 TLDs)

---

## 2. Technical Approach

### Cloudflare SDK

The tool uses the official **`cloudflare`** TypeScript SDK rather than manual `fetch()` calls. The SDK provides type-safe API access, automatic authentication, built-in retry logic, and configurable timeouts.

**Installation:**

```bash
bun add cloudflare
```

**Client initialisation:**

```typescript
import Cloudflare from "cloudflare";

const client = new Cloudflare({
  apiToken: process.env.CLOUDFLARE_API_TOKEN,
  timeout: 10_000, // 10 seconds per request
  maxRetries: 3, // built-in retry on 5xx and network errors
});
```

**Domain availability check:**

```typescript
const result = await client.registrar.domains.get(domainName, {
  account_id: accountId,
});
// result.available, result.can_register, result.pricing, etc.
```

**Relevant response fields:**

| Field                      | Type    | Description                                                                                  |
| -------------------------- | ------- | -------------------------------------------------------------------------------------------- |
| `available`                | boolean | Whether the domain is currently unregistered                                                 |
| `can_register`             | boolean | Whether Cloudflare can register this domain (may be false for premium or restricted domains) |
| `supported_tld`            | boolean | Whether the TLD is supported by Cloudflare Registrar                                         |
| `pricing.registration_fee` | number  | One-time registration cost in USD                                                            |
| `pricing.renewal_fee`      | number  | Annual renewal cost in USD                                                                   |

**Why the SDK over raw `fetch()`:**

- Type-safe responses — no manual type assertions or runtime shape validation needed
- Built-in retry logic with exponential backoff (`maxRetries` option) — eliminates custom retry code
- Automatic Bearer token injection from `apiToken` — no manual header construction
- Per-request timeout and retry overrides — can tune per call if needed
- Maintained by Cloudflare — tracks API changes automatically

### Account ID Resolution

The `account_id` is required for all API calls. Two approaches:

1. **Environment variable** (preferred): `CLOUDFLARE_ACCOUNT_ID`
2. **Auto-detect via SDK**: Call `client.accounts.list()` to enumerate accounts, use the first (or only) account. If multiple accounts exist, display the list and prompt the user to specify via the environment variable.

### Pacing Strategy

Rather than relying on reactive rate limit detection (parsing 429 responses, backoff loops), the tool proactively paces requests to stay permanently under the API rate limit. Requests are spread across a **minimum floor of 120 seconds**, regardless of how fast the API responds.

| Parameter               | Value       | Rationale                                                                                                                                 |
| ----------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Minimum total runtime   | 120 seconds | 422 requests over 120 seconds = 3.5 req/s, safely under the 4 req/s average (1,200 req/5min)                                              |
| Inter-request delay     | ~284 ms     | 120,000 ms ÷ 422 TLDs. Adjusted dynamically: if a request takes 500 ms, the added delay is only ~284 ms minus elapsed time                |
| Max concurrent requests | 1           | Sequential requests with pacing delay. Concurrency is unnecessary when the bottleneck is the deliberate pacing, not the API response time |
| Request timeout         | 10 seconds  | Configured via Cloudflare SDK `timeout` option. API typically responds in under 1 second; 10 seconds accommodates transient slowness      |
| Retry count             | 3           | Handled by the Cloudflare SDK's built-in `maxRetries` with exponential backoff. Retried requests do not skip the pacing delay             |

**Pacing for filtered runs:** When using `--popular` (~20 TLDs) or `--short` (~60 TLDs), the 120-second floor does not apply. These subsets are small enough that they complete well within the rate limit window without pacing.

### Rate Limit Safety Net

Despite proactive pacing, a 429 response is still handled as a safety net (e.g. if other API consumers share the same account's rate limit window):

1. On 429: read `Retry-After` or `X-RateLimit-Reset` header
2. Pause for the indicated duration plus 1 second of padding
3. Resume at the same pacing rate
4. Log a warning to stderr: `Rate limited by Cloudflare API — pausing for {n} seconds`

### Output Formats

**Table (default):** Rendered via **OpenTUI** (`@opentui/core`) using the imperative API. A `BoxRenderable` container with flexbox layout holds rows of `TextRenderable` components. Colour-coded using OpenTUI's `fg()` and `bold()` style functions: green for available, red for unavailable, yellow for cannot register. Progress indication rendered as a live-updating `TextRenderable` on a separate line.

```typescript
import {
  createCliRenderer,
  BoxRenderable,
  TextRenderable,
  t,
  fg,
  bold,
} from "@opentui/core";

// Example: colour-coded domain result row
const row = new TextRenderable(renderer, {
  id: `result-${domain}`,
  content: t`${fg("#00FF00")(bold(domain))}  available  $${price}`,
});
```

**JSON (`--json`):** Array of result objects to stdout via `JSON.stringify()`. OpenTUI renderer is not initialised in JSON mode — plain stdout only. Suitable for piping to `jq` or other tools.

**Quiet (`--quiet`):** Only print available domain names, one per line, via plain `console.log()`. OpenTUI renderer is not initialised in quiet mode. Suitable for piping to `xargs` or `wc -l`.

---

## 3. Requirements

### Functional Requirements

| ID     | Requirement                                                                                        | Priority | Acceptance Criteria                                                                                                                                                                                                                          |
| ------ | -------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FR-001 | Accept a single positional argument: the domain name without TLD (e.g. `example`)                  | P0       | `domain-checker example` checks `example.com`, `example.io`, etc. across all 422 TLDs                                                                                                                                                        |
| FR-002 | Read `CLOUDFLARE_API_TOKEN` from environment                                                       | P0       | Exits with code 1 and a descriptive error message if the variable is unset or empty                                                                                                                                                          |
| FR-003 | Read `CLOUDFLARE_ACCOUNT_ID` from environment, with fallback to auto-detection via `GET /accounts` | P0       | Uses env var if set; otherwise calls the accounts API and uses the result. Exits with code 1 if neither yields an account ID                                                                                                                 |
| FR-004 | Check availability of `{name}.{tld}` for each of the 422 supported TLDs                            | P0       | All 422 TLDs are queried. Failed individual checks are reported but do not abort the run                                                                                                                                                     |
| FR-005 | Display results in a formatted, colour-coded table rendered via OpenTUI                            | P0       | Table columns: Domain, Available, Can Register, Reg. Price, Renewal Price. Green rows for available domains, red for unavailable. Rendered using `@opentui/core` imperative API with `BoxRenderable` layout and `TextRenderable` styled text |
| FR-006 | Support `--json` flag for JSON output                                                              | P0       | Outputs a JSON array to stdout containing all results. No colour codes or table formatting in JSON mode                                                                                                                                      |
| FR-007 | Support `--quiet` flag for minimal output                                                          | P1       | Prints only available domain names, one per line, with no headers or decoration                                                                                                                                                              |
| FR-008 | Support `--available-only` flag to filter results                                                  | P1       | In table mode, only displays rows where `available` is `true`                                                                                                                                                                                |
| FR-009 | Show a progress indicator during execution                                                         | P1       | Displays a progress bar or counter (e.g. `[142/422] Checking domains...`) on stderr so it does not interfere with piped stdout. For full runs, also shows estimated time remaining based on the 120-second pacing floor                      |
| FR-010 | Support `--popular` flag to check only the curated popular TLD subset                              | P1       | Checks approximately 20 TLDs: `com`, `net`, `org`, `io`, `dev`, `app`, `co`, `me`, `ai`, `xyz`, `sh`, `cc`, `fm`, `tv`, `cloud`, `design`, `blog`, `shop`, `tech`, `site`. Completes in under 10 seconds. No pacing delay applied            |
| FR-011 | Support `--short` flag to check only TLDs of 3 characters or fewer                                 | P1       | Filters the TLD list to entries where the full TLD string is ≤ 3 characters (e.g. `com`, `ai`, `dev`, `io` — excludes compound TLDs like `co.uk`, `com.ai`). Completes in under 30 seconds. No pacing delay applied                          |
| FR-012 | Support `--tld <tld>` flag to check a single specific TLD                                          | P2       | Checks only the specified TLD instead of all 422. No pacing delay applied                                                                                                                                                                    |
| FR-013 | Sort results: available domains first, then alphabetically by TLD                                  | P1       | Default sort order in table and JSON output                                                                                                                                                                                                  |
| FR-014 | Pace requests over a minimum of 120 seconds for full TLD runs                                      | P0       | When checking all 422 TLDs (no `--popular`, `--short`, or `--tld` flag), requests are spread across at least 120 seconds with ~284 ms inter-request delay. Filtered runs are exempt from pacing                                              |

### Non-Functional Requirements

| ID      | Category    | Requirement                        | Target                                                                                                                 |
| ------- | ----------- | ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| NFR-001 | Performance | Complete a full 422-TLD check      | Within 120–150 seconds (pacing-limited, not network-limited). `--popular` under 10 seconds, `--short` under 30 seconds |
| NFR-002 | Reliability | Handle transient API failures      | Retry up to 3 times with exponential backoff; report failures per-TLD without aborting                                 |
| NFR-003 | Portability | Run on macOS and Linux             | No platform-specific dependencies; Bun runtime only                                                                    |
| NFR-004 | Usability   | Provide clear error messages       | All error messages include: what failed, why, and what the user can do about it                                        |
| NFR-005 | Security    | Never log or display the API token | Token must not appear in stdout, stderr, or any log output                                                             |
| NFR-006 | Correctness | Match Cloudflare dashboard results | For any given domain, the `available` field must match what the Cloudflare dashboard shows                             |

---

## 4. TLD List

The following 422 TLDs are supported by Cloudflare Registrar as of March 2026. The tool checks `{name}.{tld}` for each entry.

<details>
<summary>Full TLD list (422 entries, click to expand)</summary>

#### A

`ab.ca` · `ac` · `academy` · `accountant` · `accountants` · `actor` · `adult` · `agency` · `ai` · `airforce` · `apartments` · `app` · `army` · `associates` · `attorney` · `auction` · `audio`

#### B

`baby` · `band` · `bar` · `bargains` · `bc.ca` · `beer` · `bet` · `bid` · `bike` · `bingo` · `biz` · `black` · `blog` · `blue` · `boo` · `boston` · `boutique` · `broker` · `build` · `builders` · `business`

#### C

`ca` · `cab` · `cafe` · `cam` · `camera` · `camp` · `capital` · `cards` · `care` · `careers` · `casa` · `cash` · `casino` · `catering` · `cc` · `center` · `ceo` · `charity` · `chat` · `cheap` · `christmas` · `church` · `city` · `claims` · `cleaning` · `clinic` · `clothing` · `cloud` · `club` · `co` · `co.nz` · `co.uk` · `coach` · `codes` · `coffee` · `college` · `com` · `com.ai` · `com.co` · `com.mx` · `community` · `company` · `compare` · `computer` · `condos` · `construction` · `consulting` · `contact` · `contractors` · `cooking` · `cool` · `coupons` · `credit` · `creditcard` · `cricket` · `cruises`

#### D

`dad` · `dance` · `date` · `dating` · `day` · `dealer` · `deals` · `degree` · `delivery` · `democrat` · `dental` · `dentist` · `design` · `dev` · `diamonds` · `diet` · `digital` · `direct` · `directory` · `discount` · `doctor` · `dog` · `domains` · `download`

#### E

`education` · `email` · `energy` · `engineer` · `engineering` · `enterprises` · `equipment` · `esq` · `estate` · `events` · `exchange` · `expert` · `exposed` · `express`

#### F

`fail` · `faith` · `family` · `fan` · `fans` · `farm` · `fashion` · `feedback` · `finance` · `financial` · `fish` · `fishing` · `fit` · `fitness` · `flights` · `florist` · `flowers` · `fm` · `foo` · `football` · `forex` · `forsale` · `forum` · `foundation` · `fun` · `fund` · `furniture` · `futbol` · `fyi`

#### G

`gallery` · `game` · `games` · `garden` · `geek.nz` · `gifts` · `gives` · `giving` · `glass` · `global` · `gmbh` · `gold` · `golf` · `graphics` · `gratis` · `green` · `gripe` · `group` · `guide` · `guitars` · `guru`

#### H

`haus` · `health` · `healthcare` · `help` · `hockey` · `holdings` · `holiday` · `horse` · `hospital` · `host` · `hosting` · `house` · `how`

#### I

`icu` · `immo` · `immobilien` · `inc` · `industries` · `info` · `ing` · `ink` · `institute` · `insure` · `international` · `investments` · `io` · `irish`

#### J

`jetzt` · `jewelry`

#### K

`kaufen` · `kim` · `kitchen`

#### L

`land` · `lawyer` · `lease` · `legal` · `lgbt` · `life` · `lighting` · `limited` · `limo` · `link` · `live` · `loan` · `loans` · `lol` · `love` · `ltd` · `luxe`

#### M

`maison` · `management` · `market` · `marketing` · `markets` · `mb.ca` · `mba` · `me` · `me.uk` · `media` · `meme` · `memorial` · `men` · `miami` · `mobi` · `moda` · `mom` · `money` · `monster` · `mortgage` · `mov` · `movie` · `mx`

#### N

`navy` · `nb.ca` · `net` · `net.ai` · `net.co` · `net.nz` · `net.uk` · `network` · `new` · `news` · `nexus` · `ngo` · `ninja` · `nl.ca` · `nom.co` · `ns.ca` · `nt.ca` · `nu.ca` · `nz`

#### O

`observer` · `off.ai` · `on.ca` · `ong` · `online` · `org` · `org.ai` · `org.mx` · `org.nz` · `org.uk` · `organic`

#### P

`page` · `partners` · `parts` · `party` · `pe.ca` · `pet` · `phd` · `photography` · `photos` · `pics` · `pictures` · `pink` · `pizza` · `place` · `plumbing` · `plus` · `porn` · `press` · `pro` · `productions` · `prof` · `promo` · `properties` · `protection` · `pub`

#### Q

`qc.ca`

#### R

`racing` · `realty` · `recipes` · `red` · `rehab` · `reise` · `reisen` · `rent` · `rentals` · `repair` · `report` · `republican` · `rest` · `restaurant` · `review` · `reviews` · `rip` · `rocks` · `rodeo` · `rsvp` · `run`

#### S

`sale` · `salon` · `sarl` · `school` · `schule` · `science` · `security` · `select` · `services` · `sex` · `sh` · `shoes` · `shop` · `shopping` · `show` · `singles` · `site` · `sk.ca` · `ski` · `soccer` · `social` · `software` · `solar` · `solutions` · `soy` · `space` · `storage` · `store` · `stream` · `studio` · `style` · `supplies` · `supply` · `support` · `surf` · `surgery` · `systems`

#### T

`tax` · `taxi` · `team` · `tech` · `technology` · `tennis` · `theater` · `theatre` · `tienda` · `tips` · `tires` · `today` · `tools` · `toronto.on.ca` · `tours` · `town` · `toys` · `trade` · `trading` · `training` · `travel` · `tv`

#### U

`uk` · `university` · `uno` · `us`

#### V

`vacations` · `ventures` · `vet` · `viajes` · `video` · `villas` · `vin` · `vip` · `vision` · `vodka` · `voyage`

#### W

`watch` · `webcam` · `website` · `wedding` · `wiki` · `win` · `wine` · `work` · `works` · `world` · `wtf`

#### X

`xxx` · `xyz`

#### Y

`yk.ca` · `yoga` · `yt.ca`

#### Z

`zone`

</details>

**Maintenance note:** This list should be stored as a data file (e.g. `tlds.json`) in the project, not hardcoded inline. When Cloudflare adds or removes TLDs, only the data file needs updating.

---

## 5. Implementation Checklist

### Phase 1: Project Scaffolding

- [ ] Initialise Bun project with `bun init`
- [ ] Configure TypeScript (`tsconfig.json`) with strict mode enabled
- [ ] Install dependencies:
  - `commander` and `@commander-js/extra-typings` — CLI argument parsing with full TypeScript type inference
  - `cloudflare` — official Cloudflare TypeScript SDK (API client, auth, retries)
  - `@opentui/core` — terminal UI rendering (styled tables, progress display, colour-coded output)
- [ ] Create project structure:
  ```plaintext
  src/
    index.ts          # CLI entry point (commander setup)
    checker.ts        # Domain checking orchestration and pacing
    cloudflare.ts     # Cloudflare SDK client wrapper (initialisation, account resolution)
    ui.ts             # OpenTUI renderer, table layout, progress display
    formatter.ts      # JSON and quiet output formatters (non-TUI modes)
    pacer.ts          # Request pacing delay logic
    tlds.ts           # TLD list, popular subset, and short filter
    tlds.json         # TLD list data file
  tests/
    checker.test.ts
    cloudflare.test.ts
    ui.test.ts
    formatter.test.ts
    pacer.test.ts
    tlds.test.ts
  ```
- [ ] Add `bin` field to `package.json` pointing to `src/index.ts`
- [ ] Verify `bun run src/index.ts --help` prints usage information

### Phase 2: Cloudflare SDK Client

- [ ] Initialise `Cloudflare` client from the `cloudflare` SDK with `apiToken`, `timeout: 10_000`, and `maxRetries: 3`
- [ ] Implement account ID resolution: read `CLOUDFLARE_ACCOUNT_ID` from env, fallback to `client.accounts.list()`. If multiple accounts found, display list and exit with actionable error
- [ ] Implement single-domain availability check via `client.registrar.domains.get(domainName, { account_id })`
- [ ] Map SDK response to a typed result: `{ domain, tld, available, canRegister, registrationFee, renewalFee }`
- [ ] Handle SDK error types: authentication errors (401/403), not found (404), rate limited (429), and unexpected errors. Display actionable messages for permission issues (list required token scopes)
- [ ] Write tests using fixture responses served by a local `Bun.serve()` test server with the Cloudflare SDK's `baseURL` override pointed at `http://localhost:{port}` — no live API calls in the test suite
- [ ] Add 1–2 optional live smoke tests (gated behind `LIVE_TEST=1`) that verify a single known domain against the real Cloudflare API

### Phase 3: Request Pacing

- [ ] Implement a paced request dispatcher: sequential calls to the Cloudflare SDK with configurable inter-request delay (~284 ms for full runs)
- [ ] Implement pacing bypass for filtered runs (`--popular`, `--short`, `--tld`) — these subsets are small enough to run without delay
- [ ] Timeout and retry logic is delegated to the Cloudflare SDK (`timeout: 10_000`, `maxRetries: 3`) — the pacer only controls inter-request spacing
- [ ] Implement 429 safety net: catch SDK rate limit errors, parse retry delay, pause all dispatching, log warning to stderr, resume at same pacing rate
- [ ] Write tests for pacing dispatcher (verify inter-request timing, bypass for filtered runs — all using fixture responses via SDK `baseURL` override)

### Phase 4: CLI Interface

- [ ] Set up Commander using `@commander-js/extra-typings` for full TypeScript type inference on parsed options
- [ ] Configure programme name, version (from `package.json`), and description
- [ ] Add positional argument: `<name>` (the domain name to check)
- [ ] Add flags: `--json`, `--quiet`, `--available-only`, `--popular`, `--short`, `--tld <tld>`
- [ ] Validate environment variables on startup; exit with code 1 and actionable error if missing
- [ ] Route output mode: `--json` or `--quiet` → plain formatters (no TUI); default → OpenTUI renderer
- [ ] Connect CLI to checker, pacer, and output modules

### Phase 5: Output and UI

- [ ] Implement OpenTUI table renderer (`ui.ts`): initialise `createCliRenderer()`, compose `BoxRenderable` container with `TextRenderable` rows using flexbox layout
- [ ] Implement colour-coded result rows using OpenTUI's `t` template literal with `fg()` and `bold()` style functions: green (`#00FF00`) for available, red (`#FF0000`) for unavailable, yellow (`#FFFF00`) for available but cannot register
- [ ] Implement live-updating progress display as a `TextRenderable` that updates its `content` property as results arrive (e.g. `[142/422] Checking domains... ~78s remaining`)
- [ ] Implement JSON formatter (`formatter.ts`): `JSON.stringify()` array to stdout. OpenTUI renderer is NOT initialised in `--json` mode
- [ ] Implement quiet formatter (`formatter.ts`): `console.log()` per available domain. OpenTUI renderer is NOT initialised in `--quiet` mode
- [ ] Implement result sorting: available first, then alphabetical by TLD
- [ ] Write tests for JSON and quiet formatters. OpenTUI rendering tested manually (terminal output is not unit-testable)
- [ ] Verify OpenTUI output degrades gracefully in non-TTY environments (e.g. piped to a file)

### Phase 6: Testing and Validation

- [ ] Run full lint and type-check with zero errors
- [ ] Run test suite with all tests passing (fixture-based, no live API calls)
- [ ] Run optional live smoke test (`LIVE_TEST=1`) with 1–2 known domains to verify results match the Cloudflare dashboard
- [ ] Verify exit codes: 0 (success), 1 (fatal error), 2 (partial failure)
- [ ] Verify `--json` output parses correctly with `jq`
- [ ] Verify `--quiet` output pipes correctly to `wc -l`
- [ ] Verify colours are suppressed when piping stdout
- [ ] Verify `--popular` returns results for all curated TLDs
- [ ] Verify `--short` returns only TLDs with ≤ 3 characters
- [ ] Verify pacing: full run takes at least 120 seconds (check elapsed time)

---

## 6. Risks and Mitigations

| Risk                                                                                                                                                        | Probability | Impact | Mitigation                                                                                                                                                                                                                     | Contingency                                                                                                                                        |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Cloudflare API rate limiting** — 422 requests approaches the 1,200 req/5min global limit, especially if the user runs multiple checks in quick succession | Low         | Medium | Proactive pacing: requests spread over a minimum 120-second floor (~3.5 req/s), permanently under the 4 req/s average limit. 429 responses handled as a safety net with pause-and-retry                                        | If consecutive full runs are needed, the 120-second pacing naturally spaces them. Add a `--delay <ms>` override flag in a future release if needed |
| **API response format changes** — Cloudflare modifies the registrar API response structure without notice                                                   | Low         | Medium | The `cloudflare` SDK provides typed responses and is maintained by Cloudflare to track API changes. Pin to a specific SDK version in `package.json` to avoid surprise breaking changes. Fail loudly on missing expected fields | Update the `cloudflare` SDK dependency when API changes are detected. SDK changelog documents breaking changes                                     |
| **TLD list staleness** — Cloudflare adds or removes supported TLDs after the tool is released                                                               | Medium      | Medium | Store TLDs in a separate `tlds.json` data file; document how to update it                                                                                                                                                      | Add a future `--update-tlds` command that fetches the current list from Cloudflare (if an API endpoint exists)                                     |
| **Network instability** — Transient failures on some TLD checks due to DNS resolution, timeouts, or connection resets                                       | Medium      | Low    | 3 retries with exponential backoff per request; partial failure mode (exit code 2) reports which TLDs failed without aborting                                                                                                  | Log failed TLDs to stderr; allow re-running with `--tld` flag for individual retries                                                               |
| **Token permission insufficient** — User's API token lacks the `#registrar:read` permission                                                                 | Medium      | High   | Check permissions on first API call; if 403, display a specific error message listing the required permission scope                                                                                                            | Include the exact permission scope name in the error message and a link to the Cloudflare API token creation page                                  |
| **Premium/restricted domains** — Some domains may be available but not registrable through Cloudflare (premium pricing, registry restrictions)              | Low         | Low    | Display both `available` and `can_register` fields; colour-code `can_register: false` in yellow as a warning                                                                                                                   | Add a `--registrable-only` filter in a future release                                                                                              |

---

## 7. Resolved Design Decisions

All open questions from the initial draft have been resolved:

| #   | Question                                     | Decision                            | Rationale                                                                                                                                                                                                          |
| --- | -------------------------------------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | Multiple domain names per invocation?        | **Single name only**                | Multiple names × 422 TLDs exceeds the rate limit in a single window. Trivial to run the tool multiple times or wrap in a shell loop                                                                                |
| 2   | Include WHOIS/expiry data for taken domains? | **Out of scope**                    | The Cloudflare Registrar API does not expose WHOIS data for domains it does not manage. Adding a separate WHOIS library is a different tool entirely                                                               |
| 3   | Caching layer for results?                   | **No caching**                      | Domain availability is inherently volatile. Caching risks stale results. Tests use fixture data served by a local `Bun.serve()` test server, with 1–2 optional live smoke tests gated behind `LIVE_TEST=1`         |
| 4   | Custom TLD subsets?                          | **`--popular` and `--short` flags** | `--popular` checks a curated list of ~20 high-value TLDs. `--short` checks all TLDs with ≤ 3 characters (~60 TLDs). Both bypass the 120-second pacing floor. `--tld <tld>` remains available for single-TLD checks |

### Open Questions

No unresolved questions remain. If new questions arise during implementation, add them here with owner, deadline, and options.

---

## Change Log

| Version | Date       | Author | Changes                                                                                                                                                                                                                                                                                       |
| ------- | ---------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0.1     | 2026-03-11 | Dave   | Initial draft                                                                                                                                                                                                                                                                                 |
| 0.2     | 2026-03-11 | Dave   | Resolved all open questions. Added proactive pacing strategy (120s floor). Added `--popular` and `--short` filter flags. Simplified rate limiting to safety-net role. Updated testing strategy to fixture-based with optional live smoke tests                                                |
| 0.3     | 2026-03-11 | Dave   | Replaced manual `fetch()` with official `cloudflare` TypeScript SDK. Replaced raw ANSI escape codes with `@opentui/core` imperative TUI. Added `@commander-js/extra-typings` for type-safe CLI parsing. Simplified retry logic (delegated to SDK). Added `ui.ts` module for OpenTUI rendering |
