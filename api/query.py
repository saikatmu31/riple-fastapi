# api/query.py
from fastapi import APIRouter, Query, HTTPException
from services.query_service import query_news, top_news

router = APIRouter()

@router.get("/query")
async def query_news_api(q: str = Query(..., max_length=200)):
    try:
        return query_news(q)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/top-news")
async def top_news_api():
    try:
        return top_news()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
