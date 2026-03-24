
import sys
import os
from pathlib import Path
import json

# ==========================================================
# 1. FIX IMPORTS
# ==========================================================

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)


from ingestion.pdf_loader import pdf_to_images
from ingestion.text_extractor import extract_text_by_page
from ingestion.chunker import chunk_text
from ingestion.text_cleaner import clean_text, is_noise
from ingestion.enricher import enrich_chunks 

from fastapi import FastAPI
from pydantic import BaseModel 

# ==========================================================
# 2. FIX PATHS 
# ==========================================================

ROOT_DIR = os.path.abspath(os.path.join(current_dir, "..", ".."))

PDF_PATH = os.path.join(ROOT_DIR, "data", "raw", "paper-1.pdf")
OUTPUT_DIR = os.path.join(ROOT_DIR, "data", "processed", "paper1")
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")

# ==========================================================
# 3. APP & LOGIC
# ==========================================================
app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/ingest")
def run_ingestion():
    # Ensure directories exist
    Path(IMAGE_DIR).mkdir(parents=True, exist_ok=True)

    print(f"📄 Checking for PDF at: {PDF_PATH}")
    if not os.path.exists(PDF_PATH):
        return {"error": f"File not found at {PDF_PATH}"}

    print("📸 Extracting images...")
    pdf_to_images(PDF_PATH, IMAGE_DIR)
    
    print("🧠 Extracting text...")
    pages = extract_text_by_page(PDF_PATH)

    print("✂️ Cleaning & chunking text...")
    raw_chunks = []
    for page in pages:
        cleaned = clean_text(page["text"])
        if is_noise(cleaned):
            continue
        # Pass page number to chunker
        chunks = chunk_text(cleaned, page=page["page"]) 
        raw_chunks.extend(chunks)

    print("✨ Enriching chunks...")
    final_chunks = enrich_chunks(raw_chunks)

    # Save enriched chunks
    output_file = os.path.join(OUTPUT_DIR, "chunks_enriched.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_chunks, f, indent=2, ensure_ascii=False)

    msg = f"✅ Done. Saved {len(final_chunks)} enriched chunks to {output_file}"
    print(msg)
    return {"message": msg}

@app.get("/")
def read_root():
    return {"status": "Paper Insight Agent API is running"}

@app.post("/chat")
def chat_with_paper(query: Query):
   
    return {"answer": f"You asked: {query.question}. Backend pathing is fixed, but I need a brain!"}

# ==========================================================
# 4. SCRIPT ENTRY POINT
# ==========================================================
if __name__ == "__main__":
    run_ingestion()