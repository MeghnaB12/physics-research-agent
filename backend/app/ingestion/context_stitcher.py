# # backend/app/ingestion/context_stitcher.py

# from typing import List, Dict


# def stitch_context(chunks: List[Dict], window=1):
#     stitched = []

#     for i, chunk in enumerate(chunks):
#         context = ""

#         for j in range(max(0, i - window), min(len(chunks), i + window + 1)):
#             if j != i:
#                 context += chunks[j]["text"] + " "

#         chunk["context"] = context.strip()
#         stitched.append(chunk)

#     return stitched

from typing import List, Dict, Optional

def stitch_context(chunks: List[Dict], window_size: int = 1) -> List[Dict]:
    """
    Add previous and next text context to each chunk.
    Useful for LLMs to understand flow without retrieving extra chunks.
    """
    stitched_chunks = []
    
    # Sort by page and chunk_id to ensure correct order
    # Assuming chunk_id format is "page_index" (e.g., "3_0", "3_1")
    sorted_chunks = sorted(chunks, key=lambda x: (x["page"], int(x["chunk_id"].split("_")[1])))

    for i, chunk in enumerate(sorted_chunks):
        new_chunk = chunk.copy()
        
        # Get previous context
        if i > 0:
            new_chunk["prev_text"] = sorted_chunks[i - 1]["text"]
        else:
            new_chunk["prev_text"] = None
            
        # Get next context
        if i < len(sorted_chunks) - 1:
            new_chunk["next_text"] = sorted_chunks[i + 1]["text"]
        else:
            new_chunk["next_text"] = None

        stitched_chunks.append(new_chunk)

    return stitched_chunks