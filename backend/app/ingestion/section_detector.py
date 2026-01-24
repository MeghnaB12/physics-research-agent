
import re

def detect_section(text: str) -> str | None:
    """
    Returns the section name if the text looks like a header, else None.
    """
    text = text.strip()
    
    # 1. Numbered sections (e.g., "1. Introduction", "2.1 Methods")
    # Matches starting digit, optional dots/digits, then capitalized words
    match = re.match(r"^(\d+(\.\d+)*\.?)\s+([A-Z][a-zA-Z\s\-]{2,50})$", text)
    if match:
        return match.group(0)
    
    # 2. Common unnumbered headers
    keywords = [
        "Abstract", "Introduction", "Related Work", "Methodology", 
        "Experiments", "Results", "Discussion", "Conclusion", 
        "References", "Appendix", "Contents"
    ]
    
    if text in keywords:
        return text
        
    # 3. Roman Numerals (e.g., "I. Introduction")
    roman_match = re.match(r"^(I|II|III|IV|V|VI|VII|VIII|IX|X)\.\s+[A-Z]", text)
    if roman_match:
        return text

    return None