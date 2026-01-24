from typing import List, Dict
from ingestion.section_tracker import SectionTracker
from ingestion.context_stitcher import stitch_context
from ingestion.math_classifier import is_math_heavy
from ingestion.citation_extractor import extract_citations

def enrich_chunks(chunks: List[Dict]) -> List[Dict]:
    """
    Run all metadata extractors on the chunks.
    """
    section_tracker = SectionTracker()
    enriched = []

    # 1. First pass: Section detection and Metadata extraction
    for chunk in chunks:
        text = chunk["text"]
        
        # Update section tracker state
        section_tracker.update(text)
        current_section = section_tracker.get()

        # Extract other metadata
        enriched.append({
            **chunk,
            "metadata": {
                "section": current_section,
                "is_math_heavy": is_math_heavy(text),
                "citations": extract_citations(text)
            }
        })

    # 2. Second pass: Context Stitching (needs all chunks to be ready)
    stitched = stitch_context(enriched)

    return stitched