# AGENTS.md — `rp`

Guide for AI agents working in this directory. This is the `enhanced-rp` project branch of the parent `myriad` repo.

## What this is

`rp` is a rhyming passphrase generator. It picks a random anchor word, finds phonetic rhymes via the CMU Pronouncing Dictionary, filters them against the GCIDE English dictionary, wraps each side in filler words (determiners, adjectives), and appends two random digits.

Format: `"<Phrase A> / <phrase B> / <NN>"` — e.g. `"The underground parade / an undelivered accolade / 38"`.

In a TTY the user gets a Textual interface to pick a passphrase with live controls (spaces toggle, character limit, regenerate). In a pipe the tool just prints the generated passphrases.

## Layout

Single-file project. Everything lives in `main.py`:

- **Word banks** (`DETERMINERS`, `ADJECTIVES`) — hand-curated filler lists.
- **Core helpers** — `_load_real_words`, `_syllable_count`, `_is_good_anchor`, `build_anchor_pool`.
- **Phrase construction** — `_starts_with_vowel_sound`, `_pick_determiner`, `_build_phrase`, `_capitalise`.
- **Generator** — `generate(pool, real_words, limit=0, max_attempts=300)` with the couplet→single-statement descent strategy (see below).
- **CLI plumbing** — `_parse_count`, `_copy_to_clipboard`, `main`.
- **Textual UI** — `_run_interactive_app` hosts the `LimitModal` and `PassphraseApp` nested classes. The function imports `textual.*` lazily so the non-TTY path never pays the Textual import cost.

## Generator strategy

`generate()` respects an optional character limit by walking through progressively shorter output forms **for the same anchor** before drawing a new anchor:

1. **Couplet descent**: if `word_a` has good rhymes, pick `word_b` and try `total_fillers` from 4 down to 0. For each total, iterate every legal `(fillers_a, fillers_b)` split with both halves in `[0, 2]`. Return the first candidate that fits.
2. **Single-statement fallback** (limit-only): if a couplet form can't fit under a non-zero `limit` (or `word_a` has no good rhymes), drop the rhyme partner and try `"<phrase_a> / NN"` with fillers 2 → 1 → 0. This step is **skipped entirely when `limit == 0`** — unlimited generation must stay rhyming, so we redraw instead of emitting a non-rhyming phrase.
3. If neither form fits this anchor, draw a new anchor and restart. After `max_attempts` fruitless draws, raise `RuntimeError`.

The `" / NN"` two-digit suffix is always preserved. Shortest possible output is `"Abcd / 12"` (9 chars); any non-zero limit below `MIN_SINGLE_LEN` (9) is guaranteed to fail.

Constants to know:

| Constant          | Value | Meaning                                |
| ----------------- | ----- | -------------------------------------- |
| `SUFFIX_LEN`      | 5     | `" / NN"`                              |
| `COUPLET_SEP_LEN` | 3     | `" / "` between halves                 |
| `MIN_ANCHOR_LEN`  | 4     | matches the check in `_is_good_anchor` |
| `MIN_COUPLET_LEN` | 16    | `"Abcd / abcd / 12"`                   |
| `MIN_SINGLE_LEN`  | 9     | `"Abcd / 12"`                          |

## Textual UI

`_run_interactive_app(count, pool, real_words, seeded)` defines and runs two classes:

- **`LimitModal(ModalScreen[int | None])`** — centred dialog. `Input(type="integer", restrict=r"[0-9]*")` with value `"0"` pre-selected on mount (so the first digit overwrites rather than appending). ENTER validates and dismisses with the int (rejects values in 1..8 with a toast); ESC dismisses with `None`.
- **`PassphraseApp(App[str | None])`** — the picker. Centred card layout via `Screen { align: center middle }` + an inner `#card` `Container` with `width/height: auto; max-width/height: 90%`. Card auto-sizes to content; capped to 90% of terminal so it never overflows.

**Key bindings (documented in the card's key-hint label):**

| Key         | Action                                                                    |
| ----------- | ------------------------------------------------------------------------- |
| `↑` / `↓`   | navigate the passphrase list                                              |
| `x`         | toggle displayed spaces (the per-row count also updates, so it decreases) |
| `l`         | open the limit modal                                                      |
| `r`         | regenerate the current batch under the current limit                      |
| `enter`     | copy highlighted passphrase to clipboard (via `pbcopy`) and exit          |
| `esc` / `q` | exit without copying                                                      |

**Spaces toggle vs. limit enforcement** — these have two different roles and must not be conflated:

- The per-row `[N chars]` annotation reflects `len(display_form)`, so it decreases when spaces are toggled off.
- The character-limit check inside `generate()` always uses the canonical spaced length, so toggling spaces off on a batch that already fits can never push any phrase over the limit.

**Regeneration** happens in a `@work(thread=True, exclusive=True, name="regenerate")` worker. `on_worker_state_changed` swaps the batch atomically on success, or shows an error toast and leaves state untouched on failure. `exclusive=True` means spamming `r` cancels any in-flight regen rather than stacking.

## Gotchas

### `pkg_resources` shim (top of `main.py`)

The `pronouncing` library still does `from pkg_resources import resource_stream` at import time, even though the function is no longer called. `setuptools >= 82` removed `pkg_resources` entirely, so we inject a stub module before importing `pronouncing`. Do not remove the shim unless `pronouncing` publishes a release that deletes the dead import.

### Lazy Textual import

`from textual import …` lives **inside** `_run_interactive_app`, not at module top. This keeps the non-TTY path (`rp | cat`, CI usage) fast and free of Textual's dependency footprint. Keep it lazy.

### Non-TTY gate in `main()`

`if not sys.stdout.isatty(): print each; return` — Textual needs a real terminal. The gate is mandatory; never unconditionally instantiate `PassphraseApp`.

### Nested classes inside a function

`LimitModal` and `PassphraseApp` are defined inside `_run_interactive_app` because Textual's `App` wants its imports at definition time. This is deliberate — don't hoist them to module scope unless you also move the Textual imports up (and break the non-TTY optimisation above).

### macOS-only clipboard

`_copy_to_clipboard` shells out to `pbcopy`. Cross-platform support (xclip, wl-copy, Windows clipboard) is a future concern; if adding it, do the platform detection inside the helper, not at the call site.

## Development

Tool versions: Python `3.14` (pinned in `.python-version`), managed with `uv`. Repo-level linting uses Trunk.

```bash
# install / refresh deps
uv sync

# run it
uv run python main.py [count]         # default count = 5
uv run python main.py 8 | cat         # non-TTY smoke test

# format & lint (from the project root)
trunk fmt scripts/rp/main.py
trunk check scripts/rp/main.py
```

Install as a shell command: `./install.sh` (runs `pip install -e .`), then `rp [count]`.

### Headless UI testing

Textual's `run_test` pilot is the right tool for testing the UI without a TTY. It lets you query widgets, press keys, and assert on state:

```python
async with app.run_test(size=(100, 30)) as pilot:
    await pilot.pause()
    await pilot.press("r")
    await pilot.pause()
    # assert whatever
```

The existing tests in this project are manual (no test suite yet) — if you add automated tests, use pilot for UI and direct function calls for the generator.

## Conventions

- British English spelling in prose (per parent-repo style).
- `uv` for all Python package management; never call `pip` directly.
- Real service calls, not mocks (except inside tests).
- No silent failures — raise with a useful message or `notify(severity="error")` in the UI.
- Keep `main.py` single-file. If it grows past ~1000 lines, split the UI into `ui.py` rather than fragmenting the generator.
- Update `README.md` (human-facing) whenever the hotkey set or CLI signature changes. `AGENTS.md` (this file) tracks the internals.
