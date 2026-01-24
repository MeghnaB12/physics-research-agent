import re


def extract_citations(text: str):
    return re.findall(r"\[(\d+(?:,\s*\d+)*)\]", text)
