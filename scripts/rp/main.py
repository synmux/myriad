#!/usr/bin/env python3
"""Rhyming passphrase generator.

Uses the CMU Pronouncing Dictionary (via `pronouncing`) to find
phonetically-rhyming word pairs, filtered against the GNU Collaborative
International Dictionary of English (via `english-words`) to exclude
proper nouns, abbreviations, and obscurities.

Format:  "<phrase A> / <phrase B> / <two digits>"
Example: "The underground parade / an undelivered accolade / 38"

Interactive keys (in a TTY):
  up/down   navigate passphrases
  enter     copy the highlighted passphrase to the clipboard and exit
  x         toggle whether spaces are displayed (the displayed char
            count shrinks with the visible text; the limit, however, is
            always enforced against the spaced length)
  l         set a character limit (0 = no limit, min 9 when set);
            regenerates all passphrases under the new limit
  r         regenerate the current batch with the same settings
  esc / q   cancel without copying

Install:  pip install pronouncing english-words textual
Usage:    python main.py [count]
"""

import secrets
import subprocess
import sys
import types

# UGLY HACK ALERT EVERYONE LOOK THE OTHER WAY
# The `pronouncing` library has a dead `from pkg_resources import resource_stream`
# import left over from before it moved to the `cmudict` package. setuptools >=82
# removed `pkg_resources` entirely, so the import fails. Since the function is never
# called, we inject a lightweight stub module to satisfy the import.
if "pkg_resources" not in sys.modules:
    _stub = types.ModuleType("pkg_resources")
    _stub.resource_stream = None  # type: ignore[attr-defined]
    sys.modules["pkg_resources"] = _stub

import pronouncing  # noqa: E402
from english_words import get_english_words_set

# Passphrase-shape constants shared by the generator and the UI limit validator.
SUFFIX_LEN = len(" / 12")  # 5: " / NN"
COUPLET_SEP_LEN = len(" / ")  # 3: separator between phrase halves
MIN_ANCHOR_LEN = 4  # mirrors the len(word) < 4 check in _is_good_anchor
MIN_COUPLET_LEN = 2 * MIN_ANCHOR_LEN + COUPLET_SEP_LEN + SUFFIX_LEN  # 16
MIN_SINGLE_LEN = MIN_ANCHOR_LEN + SUFFIX_LEN  # 9 ("Abcd / 12")

# Filler word banks – padded onto each anchor to build short phrases.


DETERMINERS = [
    "a",
    "all",
    "another",
    "any",
    "both",
    "certain",
    "each",
    "either",
    "every",
    "few",
    "half",
    "its",
    "many",
    "most",
    "much",
    "my",
    "neither",
    "no",
    "one",
    "our",
    "several",
    "some",
    "such",
    "that",
    "the",
    "these",
    "this",
    "those",
    "various",
    "what",
    "which",
    "whose",
    "your",
]

ADJECTIVES = [
    "abundant",
    "agile",
    "airy",
    "amber",
    "bold",
    "breezy",
    "brisk",
    "bronze",
    "calm",
    "candid",
    "careful",
    "cheerful",
    "dapper",
    "daring",
    "dauntless",
    "deft",
    "dynamic",
    "eager",
    "earnest",
    "earthy",
    "ebullient",
    "electric",
    "fabled",
    "faithful",
    "fancy",
    "fearless",
    "fertile",
    "gentle",
    "gilded",
    "graceful",
    "grand",
    "gritty",
    "happy",
    "hardy",
    "harmonic",
    "hazy",
    "hopeful",
    "icy",
    "ideal",
    "immense",
    "impish",
    "intricate",
    "jaunty",
    "jazzy",
    "jolly",
    "judicious",
    "just",
    "keen",
    "kind",
    "kinetic",
    "knowing",
    "lively",
    "lucid",
    "lucky",
    "lush",
    "lyrical",
    "magnetic",
    "mellow",
    "mindful",
    "misty",
    "modern",
    "nifty",
    "nimble",
    "noble",
    "nuanced",
    "open",
    "opulent",
    "orderly",
    "organic",
    "outgoing",
    "patient",
    "playful",
    "poised",
    "polished",
    "primal",
    "quick",
    "quiet",
    "quintessential",
    "quirky",
    "radiant",
    "rapid",
    "rare",
    "refined",
    "robust",
    "sable",
    "sage",
    "serene",
    "sharp",
    "steady",
    "tactile",
    "tidy",
    "timely",
    "tranquil",
    "trusty",
    "upbeat",
    "urbane",
    "useful",
    "utopian",
    "valiant",
    "vast",
    "vibrant",
    "vigilant",
    "vital",
    "warm",
    "watchful",
    "weightless",
    "wild",
    "witty",
    "xenial",
    "xeric",
    "yare",
    "yearning",
    "yielding",
    "youthful",
    "zany",
    "zealous",
    "zen",
    "zesty",
]

# Real-word filter – GCIDE (GNU Collaborative International Dictionary of English)


def _load_real_words() -> set[str]:
    """Load a set of genuine lower-case English words."""
    return {
        w.lower() for w in get_english_words_set(["gcide_alpha_lower"]) if w.isalpha()
    }


# Helpers


def _syllable_count(word: str) -> int:
    """Estimate the number of syllables in a word using CMU pronouncing data.

    Looks up the word's phonetic representation and returns the syllable
    count derived from the first available pronunciation. Falls back to 0
    if the word has no entry in the CMU dictionary.

    Args:
        word: The word whose syllables should be counted.

    Returns:
        The estimated syllable count for the word, or 0 if unknown.
    """
    phones = pronouncing.phones_for_word(word)
    return pronouncing.syllable_count(phones[0]) if phones else 0


def _is_good_anchor(word: str, real_words: set[str]) -> bool:
    """Decide whether a word is a good anchor candidate for rhyming passphrases.

    A good anchor is a real English word of sufficient length with a
    moderate syllable count, making it readable and easy to rhyme with.

    Args:
        word: The candidate word to evaluate.
        real_words: A set of known English words used to validate the candidate.

    Returns:
        True if the word passes all anchor quality checks, otherwise False.
    """
    if word not in real_words:
        return False
    if len(word) < 4:
        return False
    sc = _syllable_count(word)
    return 2 <= sc <= 5


def build_anchor_pool(real_words: set[str]) -> list[str]:
    """Build a pool of anchor words suitable for rhyme-based passphrases.

    Anchors are common English words that appear in both the CMU
    Pronouncing Dictionary and the GCIDE word list, with acceptable
    syllable counts for use as phrase cores.

    Args:
        real_words: A set of lower-case English words used to filter
            out non-words, proper nouns, and obscure entries.

    Returns:
        A list of unique lower-case words that qualify as good anchors.
    """
    seen: set[str] = set()
    pool: list[str] = []
    for w in pronouncing.search("."):
        low = w.lower()
        if low not in seen and _is_good_anchor(low, real_words):
            seen.add(low)
            pool.append(low)
    return pool


# Phrase construction


def _starts_with_vowel_sound(word: str) -> bool:
    """Determine whether a word begins with a vowel sound for article selection.

    Uses CMU phoneme data when available to infer the initial sound and
    falls back to a simple first-letter vowel check if pronunciation is
    unknown.

    Args:
        word: The word whose leading sound should be inspected.

    Returns:
        True if the word is judged to start with a vowel sound, otherwise False.
    """
    if not word:
        return False
    phones = pronouncing.phones_for_word(word)
    if phones:
        first_phoneme = phones[0].split()[0]
        return first_phoneme[0] in "AEIOU"
    # Fallback: just check the letter.
    return word[0].lower() in "aeiou"


def _pick_determiner(next_word: str) -> str:
    """Select a determiner that agrees phonetically with the following word.

    Chooses a random determiner from the pool and adjusts "a" to "an"
    when the next word begins with a vowel sound.

    Args:
        next_word: The word that will follow the determiner.

    Returns:
        A determiner string that matches the initial sound of next_word.
    """
    det = secrets.choice(DETERMINERS)
    if det == "a" and _starts_with_vowel_sound(next_word):
        det = "an"
    return det


def _build_phrase(anchor: str, num_fillers: int) -> str:
    """Construct a short phrase around an anchor word using optional fillers.

    Depending on the requested filler count, returns the bare anchor,
    or prefixes it with a determiner, an adjective, or both.

    0 fillers: "accolade"
    1 filler : "the accolade"  /  "magnificent accolade"
    2 fillers: "the magnificent accolade"

    Args:
        anchor: The core word that the phrase should revolve around.
        num_fillers: The number of filler words (0–2) to prepend to the anchor.

    Returns:
        A phrase string containing the anchor and any chosen filler words.
    """
    if num_fillers == 0:
        return anchor
    if num_fillers == 1:
        # 50/50 determiner vs adjective
        if secrets.randbelow(2) == 0:
            return f"{_pick_determiner(anchor)} {anchor}"
        return f"{secrets.choice(ADJECTIVES)} {anchor}"
    # 2 fillers: determiner + adjective
    adj = secrets.choice(ADJECTIVES)
    det = _pick_determiner(adj)
    return f"{det} {adj} {anchor}"


# Generator


def _capitalise(phrase: str) -> str:
    """Upper-case the first character of a phrase, preserving the rest."""
    return phrase[0].upper() + phrase[1:] if phrase else phrase


def _couplet_filler_splits(total: int) -> list[tuple[int, int]]:
    """Return every legal (fillers_a, fillers_b) split for a given total.

    Each half must hold 0–2 fillers (matching the range supported by
    ``_build_phrase``), and together they must sum to ``total``. The
    splits are returned in a stable order so the descent is deterministic.

    Args:
        total: The total filler budget to distribute across both halves.

    Returns:
        A list of (fillers_a, fillers_b) pairs whose components are both
        in the range 0–2 and whose sum equals ``total``.
    """
    return [(a, total - a) for a in range(0, 3) if 0 <= total - a <= 2]


def generate(
    pool: list[str],
    real_words: set[str],
    limit: int = 0,
    max_attempts: int = 300,
) -> str:
    """Generate a single rhyming passphrase, optionally under a length budget.

    When ``limit`` is 0 the function returns the first rhyming couplet it
    builds and keeps drawing fresh anchors until one has valid rhymes —
    unlimited generation never drops to the non-rhyming form. When
    ``limit`` is set, it descends through progressively shorter forms for
    the same anchor before giving up and trying a new anchor:

    1. Couplet with filler budget ``total_fillers`` walking from 4 down
       to 0, trying every legal split within each budget.
    2. Single-statement fallback using just ``word_a``, trying filler
       counts from 2 down to 0. Only engaged when ``limit > 0``; with
       the limit disabled we skip this step and redraw instead.

    The ``/ NN`` two-digit suffix is always preserved. The shortest
    possible output is ``"Abcd / 12"`` (``MIN_SINGLE_LEN`` = 9 chars);
    setting ``limit`` below that is guaranteed to fail.

    Args:
        pool: Anchor words produced by :func:`build_anchor_pool`.
        real_words: GCIDE-backed word set used to validate rhyme candidates.
        limit: Maximum total character length, counting spaces. 0 disables
            the check entirely.
        max_attempts: Maximum number of fresh anchors to draw before
            giving up.

    Returns:
        A passphrase string whose length (including spaces) satisfies the
        limit, in the format ``"<phrase A> / <phrase B> / <two digits>"``
        or ``"<phrase> / <two digits>"`` when the single-statement
        fallback is used (only possible when ``limit > 0``).

    Raises:
        ValueError: If the anchor pool is empty.
        RuntimeError: If no phrase that fits the limit can be built
            within ``max_attempts``.
    """
    if not pool:
        raise ValueError("Anchor pool is empty; cannot generate passphrases")

    for _ in range(max_attempts):
        word_a = secrets.choice(pool)
        suffix = f" / {secrets.randbelow(90) + 10}"

        # Couplet descent: prefer the rhyming form when rhymes exist.
        rhymes = [
            r
            for r in pronouncing.rhymes(word_a)
            if r != word_a and _is_good_anchor(r, real_words)
        ]
        if rhymes:
            word_b = secrets.choice(rhymes)
            for total in range(4, -1, -1):
                for fillers_a, fillers_b in _couplet_filler_splits(total):
                    left = _capitalise(_build_phrase(word_a, fillers_a))
                    right = _build_phrase(word_b, fillers_b)
                    phrase = f"{left} / {right}{suffix}"
                    if limit == 0 or len(phrase) <= limit:
                        return phrase

        # Single-statement fallback: drop the rhyme partner entirely.
        # Only used when a character limit forces the compromise; under
        # unlimited generation we keep drawing anchors until one rhymes.
        if limit > 0:
            for fillers in (2, 1, 0):
                left = _capitalise(_build_phrase(word_a, fillers))
                phrase = f"{left}{suffix}"
                if len(phrase) <= limit:
                    return phrase

        # Neither form fit this anchor; draw a new one and try again.

    raise RuntimeError(
        f"Could not generate a passphrase under {limit} characters"
        f" after {max_attempts} attempts"
    )


# CLI


def _parse_count(argv: list[str]) -> int:
    """Parse and validate the optional CLI count argument.

    Args:
        argv: Raw command-line arguments, typically ``sys.argv``.

    Returns:
        The number of passphrases to generate.

    Raises:
        SystemExit: If an invalid or non-positive count is provided.
    """
    if len(argv) <= 1:
        return 5

    try:
        count = int(argv[1])
    except ValueError as exc:
        raise SystemExit("Count must be an integer.") from exc

    if count < 1:
        raise SystemExit("Count must be at least 1.")

    return count


def _copy_to_clipboard(text: str) -> None:
    """Copy text to the macOS system clipboard using pbcopy."""
    subprocess.run(["pbcopy"], input=text.encode(), check=True)


# Textual UI


def _run_interactive_app(
    count: int,
    pool: list[str],
    real_words: set[str],
    seeded: list[str],
) -> str | None:
    """Run the interactive Textual picker and return the chosen passphrase.

    Imported lazily inside the function so piped / non-TTY callers do
    not pay the Textual import cost.

    Args:
        count: Number of passphrases to keep in the picker list.
        pool: Anchor pool used for regeneration under a new limit.
        real_words: Word set used to validate rhyme candidates.
        seeded: Pre-generated passphrase batch to display initially.

    Returns:
        The chosen passphrase in the form the user saw on screen
        (spaces stripped if the spaces toggle was off), or None if
        the user cancelled.
    """
    from textual import work
    from textual.app import App, ComposeResult
    from textual.binding import Binding
    from textual.containers import Container, Vertical
    from textual.reactive import reactive
    from textual.screen import ModalScreen
    from textual.widgets import Input, Label, OptionList, Static
    from textual.worker import Worker, WorkerState

    class LimitModal(ModalScreen[int | None]):
        """Prompt for a character-limit integer.

        Dismisses with the validated integer (0 meaning "no limit") or
        None if the user cancels with Escape. Values between 1 and
        ``MIN_SINGLE_LEN - 1`` are rejected inline via a toast because
        no passphrase shorter than ``"Abcd / 12"`` can be built.
        """

        DEFAULT_CSS = """
        LimitModal {
            align: center middle;
        }
        LimitModal > Vertical {
            width: 50;
            height: auto;
            padding: 1 2;
            border: thick $primary;
            background: $surface;
        }
        LimitModal .hint {
            color: $text-muted;
            padding-top: 1;
        }
        """

        BINDINGS = [Binding("escape", "cancel", "Cancel", show=False)]

        def compose(self) -> ComposeResult:
            """Build the modal content."""
            yield Vertical(
                Label(f"Character limit (0 = no limit, min {MIN_SINGLE_LEN}):"),
                Input(
                    value="0",
                    type="integer",
                    restrict=r"[0-9]*",
                    id="limit-input",
                ),
                Label("ENTER: confirm · ESC: cancel", classes="hint"),
            )

        def on_mount(self) -> None:
            """Focus the input and pre-select the default so typing overwrites."""
            inp = self.query_one("#limit-input", Input)
            inp.focus()
            # Try the public action first; fall back to direct selection
            # assignment for older Textual releases that did not expose it.
            try:
                inp.action_select_all()
            except AttributeError:
                try:
                    from textual.widgets._input import Selection

                    inp.selection = Selection(0, len(inp.value))
                except Exception:
                    # Last-resort: clear the value so the first keystroke
                    # becomes the whole input.
                    inp.value = ""

        def on_input_submitted(self, event: Input.Submitted) -> None:
            """Validate and dismiss with the parsed integer."""
            raw = event.value.strip()
            value = int(raw) if raw else 0
            if value != 0 and value < MIN_SINGLE_LEN:
                self.app.notify(
                    f"Limit must be 0 or at least {MIN_SINGLE_LEN} characters.",
                    severity="error",
                )
                return
            self.dismiss(value)

        def action_cancel(self) -> None:
            """Dismiss without returning a new limit."""
            self.dismiss(None)

    class PassphraseApp(App[str | None]):
        """Interactive picker for rhyming passphrases.

        The app takes over the whole terminal, but the actual UI is a
        self-sizing card centred on screen. The card expands to fit the
        widest rendered row and contracts again when a tight character
        limit makes the passphrases shorter.
        """

        CSS = """
        Screen {
            align: center middle;
            background: $background;
        }
        #card {
            width: auto;
            height: auto;
            max-width: 90%;
            max-height: 90%;
            padding: 1 2;
            border: thick $primary;
            background: $surface;
        }
        #status-bar {
            width: 100%;
            height: 1;
            background: $primary 30%;
            color: $text;
            padding: 0 1;
            margin-bottom: 1;
        }
        #passphrase-list {
            width: auto;
            height: auto;
            max-height: 20;
            border: none;
            padding: 0;
            background: $surface;
        }
        #key-hints {
            width: 100%;
            height: 1;
            color: $text-muted;
            margin-top: 1;
            text-align: center;
        }
        """

        BINDINGS = [
            Binding("x", "toggle_spaces", "Toggle spaces"),
            Binding("l", "set_limit", "Set limit"),
            Binding("r", "regenerate", "Regenerate"),
            Binding("escape", "cancel", "Cancel"),
            Binding("q", "cancel", "Cancel", show=False),
        ]

        spaces_on: reactive[bool] = reactive(True)
        limit: reactive[int] = reactive(0)

        def __init__(
            self,
            count: int,
            pool: list[str],
            real_words: set[str],
            seeded: list[str],
        ) -> None:
            super().__init__()
            self._count = count
            self._pool = pool
            self._real_words = real_words
            self._passphrases: list[str] = list(seeded)
            # Pending-limit state lets on_worker_state_changed know what
            # limit the in-flight regeneration is targeting, and what to
            # report if it fails.
            self._pending_limit: int | None = None

        def compose(self) -> ComposeResult:
            """Build the main-screen layout as a centred card."""
            yield Container(
                Static(self._status_text(), id="status-bar"),
                OptionList(id="passphrase-list"),
                Static(
                    "x: toggle spaces  ·  l: set limit  ·  r: regenerate"
                    "  ·  enter: copy  ·  esc: cancel",
                    id="key-hints",
                ),
                id="card",
            )

        def on_mount(self) -> None:
            """Populate the list with the seeded batch."""
            self._refresh_list()

        # Rendering helpers

        def _status_text(self) -> str:
            pool_size = f"{len(self._pool):,}"
            limit_txt = "none" if self.limit == 0 else str(self.limit)
            spaces_txt = "on" if self.spaces_on else "off"
            return (
                f" Pool: {pool_size}  ·  Limit: {limit_txt}"
                f"  ·  Spaces: {spaces_txt}"
            )

        def _display_form(self, spaced: str) -> str:
            """Return the passphrase in its current display form.

            Strips interior spaces when the toggle is off. The canonical
            (spaced) string is never mutated.
            """
            return spaced if self.spaces_on else spaced.replace(" ", "")

        def _refresh_status(self) -> None:
            self.query_one("#status-bar", Static).update(self._status_text())

        def _refresh_list(self) -> None:
            option_list = self.query_one("#passphrase-list", OptionList)
            previous = option_list.highlighted
            option_list.clear_options()

            if self._passphrases:
                # Char count reflects the displayed form so it decreases
                # when spaces are toggled off. Limit enforcement still
                # uses the canonical spaced length inside ``generate``,
                # which is what the user-facing count converges to when
                # spaces are on.
                display_forms = [self._display_form(p) for p in self._passphrases]
                column_width = max(len(d) for d in display_forms)
                rows = [
                    f"{display:<{column_width}}  [{len(display)} chars]"
                    for display in display_forms
                ]
                option_list.add_options(rows)

                if previous is None or previous >= len(self._passphrases):
                    option_list.highlighted = 0
                else:
                    option_list.highlighted = previous

        # Actions

        def action_toggle_spaces(self) -> None:
            """Flip the display-spaces toggle; no regeneration needed."""
            self.spaces_on = not self.spaces_on
            self._refresh_list()
            self._refresh_status()

        def action_set_limit(self) -> None:
            """Prompt for a new character limit and regenerate if accepted."""

            def handle(new_limit: int | None) -> None:
                if new_limit is None or new_limit == self.limit:
                    return
                self._regenerate_under(new_limit)

            self.push_screen(LimitModal(), handle)

        def action_regenerate(self) -> None:
            """Draw a fresh batch of passphrases under the current limit."""
            self._regenerate_under(self.limit)

        def action_cancel(self) -> None:
            """Exit without copying anything."""
            self.exit(None)

        # Regeneration

        @work(thread=True, exclusive=True, name="regenerate")
        def _regenerate_worker(self, new_limit: int) -> list[str]:
            """Regenerate the passphrase batch on a worker thread.

            Returning normally signals success; raising ``RuntimeError``
            signals failure. Both cases land in ``on_worker_state_changed``
            so UI updates happen on the main thread.
            """
            return [
                generate(self._pool, self._real_words, limit=new_limit)
                for _ in range(self._count)
            ]

        def _regenerate_under(self, new_limit: int) -> None:
            """Kick off a background regeneration under ``new_limit``."""
            self._pending_limit = new_limit
            self._regenerate_worker(new_limit)

        def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
            """Swap in the regenerated batch, or roll back on failure."""
            if event.worker.name != "regenerate":
                return
            pending = self._pending_limit
            if pending is None:
                return

            if event.state is WorkerState.SUCCESS:
                result = event.worker.result
                if isinstance(result, list):
                    self.limit = pending
                    self._passphrases = result
                    self._refresh_list()
                    self._refresh_status()
                self._pending_limit = None
            elif event.state is WorkerState.ERROR:
                self.notify(
                    f"Could not fit {self._count} passphrases under "
                    f"{pending} characters.",
                    severity="error",
                )
                self.notify(
                    f"Keeping previous limit "
                    f"({'none' if self.limit == 0 else self.limit}).",
                    severity="warning",
                )
                self._pending_limit = None

        # Selection

        def on_option_list_option_selected(
            self, event: OptionList.OptionSelected
        ) -> None:
            """Copy the highlighted passphrase's displayed form and exit."""
            index = event.option_index
            if index is None or index < 0 or index >= len(self._passphrases):
                return
            chosen = self._passphrases[index]
            self.exit(self._display_form(chosen))

    app = PassphraseApp(count=count, pool=pool, real_words=real_words, seeded=seeded)
    return app.run()


def main() -> None:
    """Run the rhyming passphrase generator with interactive selection.

    Parses an optional count argument, builds the word pool, generates
    an initial batch of passphrases, and (in a TTY) hands control to
    the Textual picker. The selected passphrase is copied to the system
    clipboard. Falls back to plain stdout output when not connected to
    a terminal.
    """
    count = _parse_count(sys.argv)

    real_words = _load_real_words()
    pool = build_anchor_pool(real_words)
    print(f"Anchor pool: {len(pool):,} words\n")

    passphrases = [generate(pool, real_words) for _ in range(count)]

    if not sys.stdout.isatty():
        for passphrase in passphrases:
            print(passphrase)
        return

    chosen = _run_interactive_app(count, pool, real_words, passphrases)
    if chosen is None:
        print("No passphrase selected.")
        return

    _copy_to_clipboard(chosen)
    print(f"Copied to clipboard: {chosen}")


if __name__ == "__main__":
    main()
