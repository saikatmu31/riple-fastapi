
import re

def preprocess_text(text: str) -> str:
    """Cleans and normalizes text for better embedding results."""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)  # Normalize whitespace
    text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
    text = text.strip()
    return text
