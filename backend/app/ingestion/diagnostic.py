import json
from collections import Counter

def run_diagnostics():
    with open("data/processed/paper1/chunks_enriched.json", "r") as f:
        chunks = json.load(f)
    
    total = len(chunks)
    
    # 1. Check Sections
    sections = [c["metadata"]["section"] for c in chunks]
    section_counts = Counter(sections)
    
    # 2. Check Math
    math_heavy_count = sum(1 for c in chunks if c["metadata"]["is_math_heavy"])
    
    # 3. Check Citations
    citation_count = sum(1 for c in chunks if c["metadata"]["citations"])
    
    print(f"--- DIAGNOSTICS (Total Chunks: {total}) ---")
    print(f"🧮 Math Heavy Chunks: {math_heavy_count} ({math_heavy_count/total:.1%})")
    print(f"📚 Chunks with Citations: {citation_count}")
    print("\n🔍 Section Distribution:")
    for sec, count in section_counts.items():
        print(f"   - {sec}: {count}")

    if section_counts["Uncategorized"] == total:
        print("\n⚠️  WARNING: No sections detected. Section Tracker regex might need tuning.")
    else:
        print("\n✅ Sections are being detected.")

if __name__ == "__main__":
    run_diagnostics()