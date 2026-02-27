#!/usr/bin/env python3
"""Rhyming passphrase generator.

Uses the CMU Pronouncing Dictionary (via `pronouncing`) to find
phonetically-rhyming word pairs, filtered against Webster's Second
International Dictionary (via `english-words`) to exclude proper
nouns, abbreviations, and obscurities.

Format:  "<phrase A> / <phrase B> / <two digits>"
Example: "The underground parade / an undelivered accolade / 38"

NOTE: REQUIRES setuptools<=81.0.0

Install:  pip install pronouncing english-words
Usage:    python rhyming_passphrase.py [count]
"""

import secrets
import sys

import pronouncing
from english_words import get_english_words_set

# ---------------------------------------------------------------------------
# Filler word banks – padded onto each anchor to build short phrases.
# ---------------------------------------------------------------------------

DETERMINERS = [
    "the",
    "a",
    "this",
    "that",
    "some",
    "every",
    "each",
    "no",
    "my",
    "our",
    "your",
]

ADJECTIVES = [
    "ancient",
    "brilliant",
    "curious",
    "dangerous",
    "elegant",
    "forgotten",
    "generous",
    "hidden",
    "impossible",
    "jubilant",
    "legendary",
    "magnificent",
    "notorious",
    "obsolete",
    "peculiar",
    "remarkable",
    "spectacular",
    "tremendous",
    "underground",
    "vivid",
    "whimsical",
    "abandoned",
    "beloved",
    "celestial",
    "delicate",
    "enormous",
    "ferocious",
    "glorious",
    "heroic",
    "infinite",
    "luminous",
    "mysterious",
    "original",
    "perpetual",
    "reluctant",
    "sensitive",
    "turbulent",
    "uncertain",
    "volatile",
    "wandering",
]


# ---------------------------------------------------------------------------
# Real-word filter – Webster's Second International Dictionary
# ---------------------------------------------------------------------------


def _load_real_words() -> set[str]:
    """Load a set of genuine lower-case English words."""
    return {w.lower() for w in get_english_words_set(["web2"]) if w.isalpha()}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _syllable_count(word: str) -> int:
    phones = pronouncing.phones_for_word(word)
    return pronouncing.syllable_count(phones[0]) if phones else 0


def _is_good_anchor(word: str, real_words: set[str]) -> bool:
    """A word is a good anchor if it's a real English word with 2–5 syllables."""
    if word not in real_words:
        return False
    if len(word) < 4:
        return False
    sc = _syllable_count(word)
    return 2 <= sc <= 5


def build_anchor_pool(real_words: set[str]) -> list[str]:
    """Every word that appears in both the CMU dict and Webster's Second."""
    seen: set[str] = set()
    pool: list[str] = []
    for w in pronouncing.search("."):
        low = w.lower()
        if low not in seen and _is_good_anchor(low, real_words):
            seen.add(low)
            pool.append(low)
    return pool


# ---------------------------------------------------------------------------
# Phrase construction
# ---------------------------------------------------------------------------


def _starts_with_vowel_sound(word: str) -> bool:
    """Check whether *word* starts with a vowel sound (for a/an choice)."""
    phones = pronouncing.phones_for_word(word)
    if phones:
        first_phoneme = phones[0].split()[0]
        return first_phoneme[0] in "AEIOU"
    # Fallback: just check the letter.
    return word[0].lower() in "aeiou"


def _pick_determiner(next_word: str) -> str:
    """Pick a random determiner, respecting a/an agreement."""
    det = secrets.choice(DETERMINERS)
    if det == "a" and _starts_with_vowel_sound(next_word):
        det = "an"
    return det


def _build_phrase(anchor: str, num_fillers: int) -> str:
    """Wrap an anchor word in 0–2 filler words.

    0 fillers → "accolade"
    1 filler  → "the accolade"  /  "magnificent accolade"
    2 fillers → "the magnificent accolade"
    """
    if num_fillers == 0:
        return anchor
    if num_fillers == 1:
        # 50/50 determiner vs adjective
        if secrets.randbelow(2) == 0:
            return f"{_pick_determiner(anchor)} {anchor}"
        return f"{secrets.choice(ADJECTIVES)} {anchor}"
    # 2 fillers → determiner + adjective
    adj = secrets.choice(ADJECTIVES)
    det = _pick_determiner(adj)
    return f"{det} {adj} {anchor}"


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------


def generate(pool: list[str], real_words: set[str], max_attempts: int = 300) -> str:
    """Generate a single rhyming passphrase.

    1. Pick a random anchor from the pool.
    2. Find its phonetic rhymes (via CMU dict), filtered for quality.
    3. Wrap each anchor in filler words (total 4–6 words).
    4. Append two random digits.
    """
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
        fillers_a = secrets.randbelow(
            min(2, total_fillers) - max(0, total_fillers - 2) + 1
        ) + max(0, total_fillers - 2)
        fillers_b = total_fillers - fillers_a

        left = _build_phrase(word_a, fillers_a)
        right = _build_phrase(word_b, fillers_b)
        digits = f"{secrets.randbelow(90) + 10}"

        left = left[0].upper() + left[1:]
        return f"{left} / {right} / {digits}"

    raise RuntimeError(f"Could not find a rhyming pair after {max_attempts} attempts")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 5

    real_words = _load_real_words()
    pool = build_anchor_pool(real_words)
    print(f"Anchor pool: {len(pool):,} words\n")

    for _ in range(count):
        print(generate(pool, real_words))


if __name__ == "__main__":
    main()
