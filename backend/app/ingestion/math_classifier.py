# # backend/app/ingestion/math_classifier.py

# import re


# def is_math_heavy(text: str) -> bool:
#     symbols = re.findall(r"[=<>±√µθ∂Σ∫]", text)
#     equations = text.count("=")

#     if equations >= 2:
#         return True

#     if len(symbols) > 10:
#         return True

#     return False

import re

def is_math_heavy(text: str, threshold: float = 0.15) -> bool:
    """
    Returns True if the text contains a significant density of math symbols.
    """
    if not text:
        return False

    # 1. LaTeX patterns (e.g., $...$, \[...\], \frac)
    latex_patterns = r"(\$.*?\$|\\\[.*?\\\]|\\[a-zA-Z]+)"
    
    # 2. Common Unicode Math Symbols found in PDF extracts
    # ∑, ∫, ∂, √, Δ, ∇, ∈, ∉, ⊂, ⊃, ∪, ∩, ≤, ≥, ≠, ≈, ≡, ±, ∞, →, ⇒, ⇔, ∥
    unicode_math = r"[∑∫∂√Δ∇∈∉⊂⊃∪∩≤≥≠≈≡±∞→⇒⇔∥πµσθΩλβγ]"

    # Calculate length matches
    latex_matches = re.findall(latex_patterns, text)
    unicode_matches = re.findall(unicode_math, text)

    # Heuristic: Count total length of math content vs total text length
    math_len = sum(len(m) for m in latex_matches) + len(unicode_matches)
    total_len = len(text)

    if total_len == 0:
        return False

    density = math_len / total_len
    
    # Lowered threshold slightly for PDF text which is often sparse
    return density > 0.05  # 5% math symbols is usually a math chunk