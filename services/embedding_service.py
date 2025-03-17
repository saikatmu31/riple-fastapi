# services/embedding_service.py
from sentence_transformers import SentenceTransformer
from utils.preprocess import preprocess_text
import logging

# Load embedding model
try:
    embedding_model = SentenceTransformer("BAAI/bge-large-en")
except Exception as e:
    logging.critical(f"Failed to load embedding model: {e}")
    raise SystemExit("Critical error: Embedding model could not be loaded.")

def generate_embedding(text: str, extended: bool) -> tuple:
    """Generate normalized embedding vector from preprocessed text."""
    try:
        processed_text = preprocess_text(text)
        expanded_text = ""
        if extended:
            from services.llama_service import expand_context
            expanded_text = expand_context(processed_text)
            processed_text = f"{processed_text} {expanded_text}".strip()
        return embedding_model.encode(processed_text, normalize_embeddings=True).tolist(), expanded_text
    except Exception as e:
        logging.error(f"Error generating embedding: {e}")
        raise Exception("Error generating embedding")
