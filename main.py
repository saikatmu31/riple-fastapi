import os
# from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
# from services.query_service import query_news
# from services.embedding_service import generate_embedding
# from services.reframe_service import reframe_question
from api import embedding,query,reframe
import logging

# Initialize FastAPI app
app = FastAPI(title="News Query API", version="1.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router)
app.include_router(embedding.router)
app.include_router(reframe.router)

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 4000))
    uvicorn.run(app, host=host, port=port)
