
from pathlib import Path
import json

from ingestion.pdf_loader import pdf_to_images
from ingestion.text_extractor import extract_text_by_page
from ingestion.chunker import chunk_text
from ingestion.text_cleaner import clean_text, is_noise
from ingestion.enricher import enrich_chunks  

PDF_PATH = "data/raw/paper-1.pdf"
OUTPUT_DIR = "data/processed/paper1"

def run_ingestion():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # --- Step 1: Images ---
    print("📄 Extracting images...")
    
    # --- Step 2: Text ---
    print("🧠 Extracting text...")
    pages = extract_text_by_page(PDF_PATH)

    # --- Step 3: Chunking ---
    print("✂️ Cleaning & chunking text...")
    raw_chunks = []

    for page in pages:
        cleaned = clean_text(page["text"])
        if is_noise(cleaned):
            continue

        chunks = chunk_text(cleaned, page=page["page"]) 
        raw_chunks.extend(chunks)

    # --- Step 4: Enrichment  ---
    print("✨ Enriching chunks (Context, Math, Sections)...")
    final_chunks = enrich_chunks(raw_chunks)

    # Save
    with open(f"{OUTPUT_DIR}/chunks_enriched.json", "w", encoding="utf-8") as f:
        json.dump(final_chunks, f, indent=2, ensure_ascii=False)

    print(f"✅ Done. Saved {len(final_chunks)} enriched chunks.")

if __name__ == "__main__":
    run_ingestion()