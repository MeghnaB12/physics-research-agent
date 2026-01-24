# # backend/app/ingestion/section_tracker.py

# class SectionTracker:
#     def __init__(self):
#         self.current_section = "Unknown"

#     def update(self, text: str):
#         from backend.app.ingestion.section_detector import detect_section

#         section = detect_section(text)
#         if section:
#             self.current_section = section

#     def get(self):
#         return self.current_section

# Changed from 'backend.app.ingestion...' to just 'ingestion...'
from ingestion.section_detector import detect_section

class SectionTracker:
    def __init__(self):
        self.current_section = "Uncategorized"

    def update(self, text: str):
        if not text:
            return

        # Check only the first line of the chunk for a header
        first_line = text.split('\n')[0].strip()
        
        # Don't switch sections on very long lines (likely just text)
        if len(first_line) > 80:
            return

        detected = detect_section(first_line)
        if detected:
            self.current_section = detected

    def get(self):
        return self.current_section