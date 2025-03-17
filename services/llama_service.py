# services/llama_service.py
from llama_cpp import Llama
from core.config import Config
import logging

# Load Mixtral 1B model
try:
    llm = Llama(
        model_path=Config.MIXTRAL_MODEL_PATH,
        n_threads=64,
        n_batch=512,
        n_ctx=2048,
        verbose=False
    )
    logging.info("Mixtral 1B model loaded successfully.")
except Exception as e:
    logging.critical(f"Failed to load Mixtral model: {e}")
    raise SystemExit("Critical error: Mixtral model could not be loaded.")

def expand_context(text: str) -> str:
    """Use Mixtral 1B to infer additional keywords for context expansion."""
    try:
        system_prompt = (
            "You are an AI assistant that enhances search queries by expanding them with relevant context. "
            "Given an input phrase, provide a list of semantically related keywords or phrases that improve search relevance. "
            "Ensure the output maintains contextual integrity without adding unnecessary or misleading terms.\n\n"
            "Input: {text}\n"
            "Output: "
        )
        prompt = system_prompt.format(text=text)
        response = llm(prompt, max_tokens=50, temperature=0.7)
        expanded_text = response["choices"][0]["text"].strip()
        return expanded_text
    except Exception as e:
        logging.error(f"Error expanding context: {e}")
        return ""
