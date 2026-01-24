
import re


def strip_headers(text: str) -> str:
    header_patterns = [
        r"THE ℓp-BOUNDEDNESS OF WAVE OPERATORS\s*\d*",
        r"SISIHUANGANDXIAOHUAYAO",
        r"\d+\s+SISIHUANGANDXIAOHUAYAO",
    ]

    for p in header_patterns:
        text = re.sub(p, "", text)

    return text


def clean_text(text: str) -> str:
    if not text:
        return ""

    # Remove PDF encoding artifacts
    text = re.sub(r"\(cid:\d+\)", "", text)

    # Strip running headers
    text = strip_headers(text)

    # Fix glued words
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)

    # Fix missing spaces after punctuation
    text = re.sub(r"([.,;:])([A-Za-z])", r"\1 \2", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def is_noise(text: str) -> bool:
    if not text or len(text) < 40:
        return True

    # Truly useless sections only
    noise_patterns = [
        r"\bReferences\b",
        r"\bContents\b",
        r"arXiv",
    ]

    return any(re.search(p, text) for p in noise_patterns)
