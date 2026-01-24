
import re


HEADER_PATTERNS = [
    r"^\d+$",
    r"^Remark\s+\d+",
    r"^Definition\s+\d+",
    r"^Lemma\s+\d+",
    r"^Theorem\s+\d+",
    r"^\(\d+\.\d+\)",
]


def is_noise_chunk(text: str) -> bool:
    if not text or len(text) < 60:
        return True

    for p in HEADER_PATTERNS:
        if re.search(p, text):
            return True

    # Too many symbols → likely broken math fragment
    symbol_ratio = sum(c in "=<>±∑√µθ" for c in text) / max(len(text), 1)
    if symbol_ratio > 0.35:
        return True

    return False
