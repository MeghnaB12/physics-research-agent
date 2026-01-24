# # import nltk
# # from nltk.tokenize import sent_tokenize

# # # Ensure required NLTK resources exist
# # def ensure_nltk():
# #     try:
# #         nltk.data.find("tokenizers/punkt")
# #     except LookupError:
# #         nltk.download("punkt")

# #     try:
# #         nltk.data.find("tokenizers/punkt_tab")
# #     except LookupError:
# #         nltk.download("punkt_tab")

# # ensure_nltk()

# # MAX_CHARS = 800

# # def chunk_text(text: str):
# #     if not text.strip():
# #         return []

# #     sentences = sent_tokenize(text)
# #     chunks = []

# #     current_chunk = ""
# #     for sent in sentences:
# #         if len(current_chunk) + len(sent) < MAX_CHARS:
# #             current_chunk += " " + sent
# #         else:
# #             chunks.append(current_chunk.strip())
# #             current_chunk = sent

# #     if current_chunk:
# #         chunks.append(current_chunk.strip())

# #     return chunks

# # backend/app/ingestion/chunker.py

# import re
# from typing import List, Dict

# from ingestion.text_cleaner import clean_text
# from ingestion.math_normalizer import normalize_math
# from ingestion.filters import is_noise_chunk


# MAX_CHUNK_SIZE = 500
# OVERLAP_SIZE = 80


# def split_sentences(text: str) -> List[str]:
#     return re.split(r"(?<=[.!?])\s+", text)


# def chunk_text(
#     text: str,
#     page: int,
# ) -> List[Dict]:

#     text = clean_text(text)
#     text = normalize_math(text)

#     sentences = split_sentences(text)

#     chunks = []
#     buffer = ""
#     chunk_id = 0

#     for sent in sentences:
#         if len(buffer) + len(sent) <= MAX_CHUNK_SIZE:
#             buffer += " " + sent
#         else:
#             chunk = buffer.strip()
#             if not is_noise_chunk(chunk):
#                 chunks.append({
#                     "page": page,
#                     "chunk_id": f"{page}_{chunk_id}",
#                     "text": chunk
#                 })
#                 chunk_id += 1

#             # overlap
#             buffer = buffer[-OVERLAP_SIZE:] + " " + sent

#     # last chunk
#     if buffer.strip() and not is_noise_chunk(buffer):
#         chunks.append({
#             "page": page,
#             "chunk_id": f"{page}_{chunk_id}",
#             "text": buffer.strip()
#         })

#     return chunks

# backend/app/ingestion/chunker.py

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
