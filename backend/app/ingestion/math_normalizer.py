import re


def normalize_math(text: str) -> str:
    if not text:
        return ""

    replacements = {
        "ℓp": "l^p",
        "ℓq": "l^q",
        "ℓ∞": "l^∞",
        "ℓ1": "l^1",
        "∆": "Δ",
        "→": "->",
        "−": "-",
        "≲": "<=",
        "≥": ">=",
        "≤": "<=",
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    # Fix glued math like: p1−p1′ → p1 - p1'
    text = re.sub(r"([a-zA-Z0-9])([-+])([a-zA-Z0-9])", r"\1 \2 \3", text)

    # Fix ||t|−1/3(p1−p1′)|
    text = re.sub(r"\|t\|\s*-\s*1\s*/\s*3", "|t|^{-1/3}", text)

    # Normalize multiple math spaces
    text = re.sub(r"\s{2,}", " ", text)

    return text.strip()
