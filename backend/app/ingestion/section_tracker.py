
from ingestion.section_detector import detect_section

class SectionTracker:
    def __init__(self):
        self.current_section = "Uncategorized"

    def update(self, text: str):
        if not text:
            return

        # Check only the first line of the chunk for a header
        first_line = text.split('\n')[0].strip()
        
        if len(first_line) > 80:
            return

        detected = detect_section(first_line)
        if detected:
            self.current_section = detected

    def get(self):
        return self.current_section