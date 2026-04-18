# `rp` — rhyming passphrase generator

Generates short, memorable passphrases built from phonetically-rhyming word pairs plus two random digits. Designed to be readable, pronounceable, and easy to transcribe.

Example output:

```plaintext
The underground parade / an undelivered accolade / 38
My yearning tailor / its xenial whaler / 67
Those nimble amyloid / such gentle android / 16
```

## Install

```sh
cd scripts/rp
./install.sh         # read it first — it runs `pip install -e .`
```

Then restart your shell. `rp` is now on your `$PATH`.

Requires Python 3.14 and macOS (for `pbcopy` clipboard support; see below).

## Usage

```sh
rp [count]     # default count = 5
```

### In a terminal

`rp` launches a compact centred picker. Use the arrow keys to highlight a passphrase, then hit enter — the selected passphrase is copied to your clipboard (via `pbcopy`) and the tool exits.

| Key         | What it does                                                                                                                                                                                                                                                                           |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `↑` / `↓`   | Move the highlight                                                                                                                                                                                                                                                                     |
| `enter`     | Copy the highlighted passphrase and exit                                                                                                                                                                                                                                               |
| `x`         | Toggle whether spaces are shown. The character count shown on each row reflects the **displayed** form — so toggling spaces off makes every count drop. The character **limit**, however, is always enforced against the spaced form, so toggling cannot push a passphrase over limit. |
| `l`         | Prompt for a character limit. Enter `0` for no limit (the default); any positive value must be at least 9 characters. Once you hit enter, the whole list regenerates so every passphrase fits under the limit (counting spaces). ESC cancels the prompt.                               |
| `r`         | Regenerate the batch with the current settings.                                                                                                                                                                                                                                        |
| `esc` / `q` | Exit without copying anything.                                                                                                                                                                                                                                                         |

When a tight limit would force shorter output, the rhyming couplet form drops filler words first (so you might see `Suttle / these rebuttal / 55` instead of the usual longer form), and below about 16 characters falls back to a single-statement form like `Half dally / 17`.

### In a pipe

If `rp` is not attached to a TTY (for example `rp 10 | cat`), it skips the picker entirely and prints the generated passphrases straight to stdout, one per line. Useful for scripting.

```sh
rp 3 | cat
# Anchor pool: 24,439 words
#
# Those nimble amyloid / such gentle android / 16
# Our bold missourian / some hopeful centurion / 84
# Any tactile contemn / much calm condemn / 84
```

## How it works

Anchor words come from the intersection of the CMU Pronouncing Dictionary (for rhymes) and the GCIDE English dictionary (to exclude proper nouns, abbreviations, and rarities). Rhymes are paired phonetically, then wrapped in determiners (`the`, `some`, `every`…) and adjectives (`nimble`, `radiant`, `zesty`…) drawn at random to build short, grammatical phrases.

All random choices use `secrets` rather than `random`, so the output is suitable for passphrase use.

## Dependencies

- [`pronouncing`](https://pypi.org/project/pronouncing/) — CMU Pronouncing Dictionary bindings
- [`english-words`](https://pypi.org/project/english-words/) — GCIDE word set for filtering
- [`textual`](https://pypi.org/project/textual/) — terminal UI

Managed via `uv`. See `pyproject.toml` for exact versions.

## Limitations

- **macOS only (for the clipboard step).** The picker shells out to `pbcopy`. The generator itself is cross-platform; only the copy step is macOS-specific.
- **No stored history.** Each run generates a fresh batch; nothing is saved between invocations.

## Contributing / hacking on it

For architecture, conventions, and gotchas (including the `pkg_resources` shim at the top of `main.py`), see [`AGENTS.md`](./AGENTS.md).
