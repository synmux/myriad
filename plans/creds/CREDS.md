# `creds`: biometric-gated secrets from 1Password into fish

Proposal only. Nothing is implemented. Date: 2026-10-24.

## Context

Today `~/.config/fish/secrets.fish` exports 99 secrets as `__NAME` and abbreviations re-alias them (`GITHUB_TOKEN=$__GITHUB_TOKEN mise …`). The `__` prefix defeats malware that looks up fixed names. It does nothing against malware that dumps the environment, and that is the common case.

Measured on this machine, read-only, during planning:

- `ps -Eww -ax` run as your user shows **all 99** `__*` secrets. Any same-user process can do that at any time, with no prompt.
- Every child process inherits them: npm scripts, language servers, Claude Code, every MCP server.
- `GITHUB_TOKEN` is also a fish **universal** variable, so it sits in plaintext in `~/.config/fish/fish_variables`.
- `~/.claude.json` carries a 1Password **service-account token** in plaintext as a `--service-account-token=` argument to `mcp-1password`. It is also visible in `ps` arguments while that server runs. The server supports `--auth-mode=desktop`.

Goal: `creds SERVICE` fetches that service's secrets from 1Password, Touch ID is required, and the secrets appear under their real names. Secrets leave shell config entirely.

## What 1Password gives you in October 2026 (verified against docs and `op --help`)

| Fact                                                                                                                                                                                                                                                                    | Consequence                                                                                                                                                                          |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `op` CLI app-integration authorisation is **per terminal tab** (tty + start time): one Touch ID, then a 10-minute inactivity session that refreshes on use, 12-hour cap, inherited by sub-shells.                                                                       | A fish function around `op` prompts once per tab, not per call. Anything spawned from that tab can run `op read` silently for the next 10 minutes.                                   |
| 1Password SDK desktop auth (Go, JS, Python; GA) is **per process and per account**, 10-minute inactivity, revoked when 1Password locks. The prompt shows the requesting executable's name.                                                                              | A short-lived `creds` binary gets a prompt on **every** call. An unknown process trying the same thing produces a visible prompt naming itself: a tripwire you do not get from `op`. |
| 1Password Environments: named sets of `KEY=VALUE`, imported from `.env`, read by `op environment read <ID>` (beta, no flags), `op run --environment <ID> -- cmd`, or SDK `Environments.GetVariables(id)` which returns `name`, `value`, `masked`. Addressed by ID only. | Natural home for "one Environment per service". Needs a small name→ID map.                                                                                                           |
| Mounted `.env` files: 1Password serves a FIFO at a path; first read prompts, then any process can read until 1Password locks.                                                                                                                                           | You already use this per project. It is not the per-call gate you asked for, so `creds` covers what the mounts do not: ad-hoc CLI work and services used across projects.            |
| `op signout` exists; its effect on an app-integration tab session is undocumented. `op environment read` has no `--reveal`; whether it masks hidden values is unverified.                                                                                               | Both are spike items if Option A is chosen.                                                                                                                                          |

Assumed, on your word: the app's Settings → Developer → "Integrate with 1Password SDKs" toggle is on, the Environments policy is on for your account, and you already mount `.env` files into dev projects. The spike confirms the first two as a side effect; nothing in the plan hedges on them.

## The three options

### Option A: a fish function around the `op` CLI

- **Where:** `~/.config/fish/functions/creds.fish`, about 40 lines, chezmoi-managed like the rest.
- **How:** `op item get $service --vault creds --format json --reveal | jq` (or `op environment read $id`), then `set -gx` each field whose label is an env var name. Secrets travel through a pipe, never through `argv`.
- **Gate:** Touch ID once per terminal tab, then silent for 10 minutes of activity.
- **Good:** zero build, zero new dependencies, uses the integration you already run for `op plugin run`.
- **Bad:** does not meet the requirement that biometrics gate every load. Malware launched from the same tab inherits the `op` session.

### Option B: a compiled `creds` binary on the official SDK, plus a 10-line fish shim

- **Language:** Go, `github.com/1password/onepassword-sdk-go` v0.4.1, `onepassword.WithDesktopAppIntegration(account)`. Go over Bun because the SDK's desktop auth is documented for Go and unverified under Bun or `bun build --compile`; a compiled binary also makes the 1Password prompt name the process `creds` instead of `bun`. Jev scored Go 0.99 against Bun, a dual spike, and fish-only, with all three per-process requirements supported.
- **How:** `creds SERVICE` looks up the service in a plain name-to-Environment-ID file, authenticates (Touch ID, every time, because it is a new process), calls `Environments().GetVariables`, and writes zero-byte-separated (NUL) `name`/`value` pairs to stdout. The fish function `creds` reads them with `read -z` and runs `set -gx`. No `eval`, no quoting bugs, nothing on `argv`.
- **Gate:** per call, by construction. Rogue callers trigger a visible prompt.
- **Good:** exactly the request; smallest exposure of the three that still export; the prompt is an audit signal.
- **Bad:** a build step, a binary to install, and friction if you load many services per hour. The decision matrix scored ergonomics 3/10 for this reason.

### Option C: scoped injection, secrets never enter the interactive shell

- **How:** `creds SERVICE -- command args` runs the command with the service's variables in **its** environment only (`op run --environment <ID> -- …`, or the Option B binary doing `exec` itself). The interactive fish process never holds a secret, so `ps -E` on the shell, later children, agents, and MCP servers cannot read them. Pairs with your existing `op plugin run` aliases and with direnv exporting `op://` references instead of values.
- **Gate:** per tab if built on `op`; per call if built on the Option B binary.
- **Good:** closest match to the stated threat; the adversarial review (six perspectives, none failed) rated the export designs' residual risk "critical" and this one lowest.
- **Bad:** it does not set the variable in the running shell, and wrapping every command is a habit change.

### Scores

Decision matrix (weights: gate 3, exposure 3, code 2, ergonomics 2, risk 1, fit 1): **B 89.0, C 83.5, A 74.5**. The only criterion where B loses badly is ergonomics.

## Recommendation: one Go binary, two modes, scoped by default

Build Option B's binary and give it Option C's behaviour as the default:

```text
creds cloudflare -- wrangler deploy     # exec mode: secrets live only in that child (default when "--" present)
creds cloudflare                        # export mode: fish shim sets CLOUDFLARE_* for 15 minutes, then erases them
creds --clear                           # erase everything export mode set
creds --list                            # names from the map file, no 1Password call
```

Export mode gets two mitigations the adversarial review asked for:

1. **Time-boxed.** The shim records a deadline; a `--on-event fish_prompt` handler erases expired variables. Default 15 minutes, `--ttl` to override. This closes the loaded-at-09:00-still-there-at-18:00 hole the auditor flagged.
2. **Visible.** The names of loaded services appear in `fish_right_prompt` (for example `🔑 cloudflare github`) so you always know what is exposed.

Storage: one 1Password **Environment per service**, variables named exactly as the env vars (`CLOUDFLARE_API_TOKEN`, not `__CLOUDFLARE_API_TOKEN`). Migration is `.env` import in the 1Password app, which you already know from the project mounts. The name-to-ID map is a plain, non-secret text file in the chezmoi-managed fish configuration. No vault-item fallback is planned.

Division of labour with what you already run: project `.env` mounts keep serving project toolchains (dotenv libraries, Docker Compose). `creds` serves the 99 shell-level keys: CLIs run outside a project directory and services shared across projects. Where a variable is needed in both places, it lives in both Environments; that duplication is deliberate and visible in the app.

Why this and not A: A fails your actual requirement and inherits the tab-session weakness. Why this and not pure C: you asked for shell export, and the scoped default plus TTL gets most of C's benefit while keeping export available when you want it.

## Ideas you did not ask for

- **The prompt is the alarm, not the wall.** Same-user malware can wait for you to authenticate. What per-process auth buys is that a second, unexpected prompt naming an unknown process is a detection you notice. Treat an unexplained prompt as an incident.
- **Fix the three live leaks first**, independent of `creds`: `set -eU GITHUB_TOKEN`; rotate the service-account token in `~/.claude.json` and switch `mcp-1password` to `--auth-mode=desktop`; stop sourcing `secrets.fish` once migrated and purge it from the chezmoi repo history.
- **Run Claude Code with no secrets at all.** With exports gone, agents and MCP servers start clean; a project needing a key uses `creds svc -- claude` or `op run`. Your memory note already records that plugin `headersHelper`s run with `TOKEN`/`SECRET`/`KEY` variables stripped, so nothing you rely on today needs them inherited.
- **Replace the `GITHUB_TOKEN=$__GITHUB_TOKEN mise …` abbreviations** with `creds github -- mise …`. Same keystrokes, no resident secret.
- **direnv + references, not values.** `.envrc` exports `SERVICE_API_KEY=op://…` strings; commands run under `op run`. No biometric spam on `cd`, no plaintext.
- **Your mounts have a weaker gate than `creds` will.** A mounted `.env` unlocks on first read and stays readable by every process until 1Password locks. Shorten the app's auto-lock interval if that window bothers you; `creds` export mode has its own TTL regardless.
- **Prefer scoped tokens.** The contrarian's warning holds: a smoother gate tempts you to use production credentials locally. Keep dev-scoped tokens in the Environments.
- **Keychain alternative** (`envchain`, `security add-generic-password` with a Touch ID ACL) works without 1Password. You want one store, so this is only the zero-dependency fallback.

## Files that would be touched (on approval, in a later plan)

- New repo `creds/`: a Go module with a single `main.go` of about 100 lines, plus tests for the map parser and the NUL writer.
- `~/.config/fish/functions/creds.fish` (shim, TTL handler, `--clear`), `~/.config/fish/conf.d/creds.fish` (prompt badge), `~/.config/fish/creds.map` (name-to-ID, non-secret), all through chezmoi.
- `~/.config/fish/secrets.fish` and `config.fish:1` removed after migration; `abbrs.fish` lines that prefix `GITHUB_TOKEN=` rewritten.
- `~/.claude.json` `mcpServers.1password` switched to desktop auth.

## Verification (how we would prove it before trusting it)

1. **Spike, 15 lines of Go:** `WithDesktopAppIntegration` + `GetVariables` on one test Environment. Run it twice in one tab. Pass: two Touch ID prompts, each naming `creds`. Fail: second run silent, in which case per-process auth is not what the docs say and the design falls back to A plus `op signout` testing.
2. **Exposure check:** after `creds svc -- env`, `ps -Eww -p $fish_pid` shows no `SVC_*`; after `creds svc`, it does, and after the TTL it does not. Count with the same `ps` pipeline used during planning.
3. **No secrets on argv:** `ps -o args= -p <creds pid>` while it runs shows only the service name.
4. **Unit tests:** map-file parsing, NUL pair encoding, TTL arithmetic in fish (through `fish -c` tests).
5. **Migration dry run:** import one service's `.env`, delete its `__` lines, open a new shell, confirm the tool that uses it still works through `creds`.
6. **Rotate** every secret that was exported while `secrets.fish` was live. They have all been readable by every process on this machine for as long as that file has existed.

## Decisions taken (2026-10-24)

1. Gate: Touch ID on every `creds` call (compiled binary, per-process SDK auth).
2. Default mode: `creds SERVICE` exports with a 15-minute TTL and a prompt badge; `creds SERVICE -- cmd` is the scoped mode.
3. Storage: one 1Password Environment per service. No vault-item fallback.
4. Language: Go.

Assumptions you confirmed: SDK integration toggle on; Environments policy on; `.env` mounts already in use for dev projects.

Next step after approval: the spike in Verification step 1, before any other code.

## Sources consulted

1Password docs: CLI app-integration security, SDK desktop-app integration security, Environments overview, `op environment` reference, local `.env` files, SDK quick start (Go and JS). `op --help` output for `environment read`, `run`, `signout`, `item get` on CLI 2.43.0-beta.02. npm metadata for `@1password/sdk` 0.5.0; Go module index for `onepassword-sdk-go` v0.4.1. Prior art: `envchain`, Gruntwork's zsh loader, jonmagic's `op run` wrapper. Reasoning: Devil's Advocate session `b7f59bde`, Decision Matrix session `creds-tool-options-2026-10-24`, Jev decision (jev-1.14.0).
