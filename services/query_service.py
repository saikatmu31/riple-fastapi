# services/query_service.py
from pymongo import MongoClient
from sentence_transformers import CrossEncoder,SentenceTransformer
from llama_cpp import Llama
from functools import lru_cache
from utils.preprocess import preprocess_text
import logging
import os

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["inkpod"]
collection = db["articles"]

# Load Models
embedding_model = SentenceTransformer("BAAI/bge-large-en")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

language_model = Llama(
    model_path="/home/azureuser/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    n_threads=64,
    n_batch=512,
    n_ctx=2048,
    verbose=False
)

# Caching Embeddings
@lru_cache(maxsize=100)
def cached_embedding(text: str):
    return embedding_model.encode(text, convert_to_tensor=True).tolist()

def build_prompt(query: str, articles: list) -> str:
    context = "\n\n".join(
        [f"[Article {i+1}]\nTitle: {doc['title']}\nContent: {doc['body'][:500]}..."
         for i, doc in enumerate(articles)]
    )
    
    return f"""[INST] You are a news assistant. Answer the question **only** using the provided articles. Do **not** use outside knowledge.  

### Articles:
{context}

### Instructions:
1. **Answer the question concisely:** {query}  
2. **Keep responses under 150 words** while maintaining completeness.  
3. **Cite sources using [Article X]** where information is used.  
4. **If the answer isn't found in the articles, respond with:**  
   "I cannot find the answer based on the given sources."  

Strictly follow these instructions.  
[/INST]  

Answer: """

def query_news(q: str):
    try:
        embedding = cached_embedding(q)
        results = collection.aggregate([
            {"$vectorSearch": {
                "queryVector": embedding,
                "path": "embedding",
                "numCandidates": 50,
                "limit": 10,
                "index": "article_embd",
                "exact": False,
            }},
            {"$sort": {"relevance": -1}}
        ])
        
        results = list(results)
        
        if not results:
            return "I couldn't find relevant news articles."
        
        article_texts = [f"{doc['title']} {doc['body']}" for doc in results]
        scores = reranker.predict([(q, text) for text in article_texts])
        reranked = [doc for _, doc in sorted(zip(scores, results), reverse=True)]
        top_articles = reranked[:3]
        
        prompt = build_prompt(q, top_articles)
        response = language_model(prompt, max_tokens=300, temperature=0.3, top_p=0.9, repeat_penalty=1.1)
        response_text = response["choices"][0]["text"].strip()
        response_text = response_text.split("\n\n[Article")[0]  # Remove artifacts
        
        return response_text
    except Exception as e:
        logging.error(f"Error querying news: {e}")
        return "Internal server error."
