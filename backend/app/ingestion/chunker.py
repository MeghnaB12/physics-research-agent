
import re
from typing import List, Dict

from ingestion.text_cleaner import clean_text
from ingestion.math_normalizer import normalize_math
from ingestion.filters import is_noise_chunk


MAX_CHUNK_SIZE = 500      # characters
OVERLAP_SIZE = 80         # characters


def split_sentences(text: str) -> List[str]:
    """Lightweight sentence splitter (math-safe)."""
    return re.split(r"(?<=[.!?])\s+", text)


def _safe_overlap(text: str, overlap_size: int) -> str:
    """
    Extract overlap without cutting mid-word.
    """
    if len(text) <= overlap_size:
        return text

    overlap = text[-overlap_size:]
    first_space = overlap.find(" ")
    return overlap[first_space + 1 :] if first_space != -1 else overlap


def chunk_text(
    text: str,
    page: int,
) -> List[Dict]:
    """
    Convert page text into overlapping, math-safe chunks.
    """

    # --- Pre-clean ---
    text = clean_text(text)
    text = normalize_math(text)

    sentences = split_sentences(text)

    chunks: List[Dict] = []
    buffer = ""
    chunk_id = 0

    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue

        # Try to add sentence to buffer
        if len(buffer) + len(sent) + 1 <= MAX_CHUNK_SIZE:
            buffer = f"{buffer} {sent}".strip()
        else:
            # Flush buffer
            if buffer and not is_noise_chunk(buffer):
                chunks.append({
                    "page": page,
                    "chunk_id": f"{page}_{chunk_id}",
                    "text": buffer
                })
                chunk_id += 1

            # Start new buffer with overlap
            overlap = _safe_overlap(buffer, OVERLAP_SIZE)
            buffer = f"{overlap} {sent}".strip()

    # Final flush
    if buffer and not is_noise_chunk(buffer):
        chunks.append({
            "page": page,
            "chunk_id": f"{page}_{chunk_id}",
            "text": buffer
        })

    return chunks
