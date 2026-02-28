#!/usr/bin/env python3
"""Rhyming passphrase generator.

Uses the CMU Pronouncing Dictionary (via `pronouncing`) to find
phonetically-rhyming word pairs, filtered against the GNU Collaborative
International Dictionary of English (via `english-words`) to exclude
proper nouns, abbreviations, and obscurities.

Format:  "<phrase A> / <phrase B> / <two digits>"
Example: "The underground parade / an undelivered accolade / 38"

Install:  pip install pronouncing english-words
Usage:    python main.py [count]
"""

import secrets
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


def generate(pool: list[str], real_words: set[str], max_attempts: int = 300) -> str:
    """Generate a single rhyming passphrase.

    1. Pick a random anchor from the pool.
    2. Find its phonetic rhymes (via CMU dict), filtered for quality.
    3. Wrap each anchor in filler words (2–4 fillers total, 4–6 words total).
    4. Append two random digits.

    Returns:
        A passphrase in the format "<phrase A> / <phrase B> / <two digits>".

    Raises:
        ValueError: If no anchor words are available in the input pool.
        RuntimeError: If no valid rhyming pair can be built within max_attempts.
    """
    if not pool:
        raise ValueError("Anchor pool is empty; cannot generate passphrases")

    for _ in range(max_attempts):
        word_a = secrets.choice(pool)
        candidates = [
            r
            for r in pronouncing.rhymes(word_a)
            if r != word_a and _is_good_anchor(r, real_words)
        ]
        if not candidates:
            continue

        word_b = secrets.choice(candidates)

        # Distribute 2–4 filler words across both halves (each half ≤ 2).
        total_fillers = secrets.randbelow(3) + 2
        min_fillers_a = max(1, total_fillers - 2)
        max_fillers_a = min(2, total_fillers - 1)
        fillers_a = secrets.randbelow(max_fillers_a - min_fillers_a + 1) + min_fillers_a
        fillers_b = total_fillers - fillers_a

        left = _build_phrase(word_a, fillers_a)
        right = _build_phrase(word_b, fillers_b)
        digits = f"{secrets.randbelow(90) + 10}"

        left = left[0].upper() + left[1:]
        return f"{left} / {right} / {digits}"

    raise RuntimeError(f"Could not find a rhyming pair after {max_attempts} attempts")


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


def main() -> None:
    """Run the rhyming passphrase generator as a CLI tool.

    Parses an optional count argument, builds the word pool, and prints
    the requested number of generated passphrases to stdout.
    """
    count = _parse_count(sys.argv)

    real_words = _load_real_words()
    pool = build_anchor_pool(real_words)
    print(f"Anchwqqqor pool: {len(pool):,} words\n")

    for _ in range(count):
        print(generate(pool, real_words))


if __name__ == "__main__":
    main()
