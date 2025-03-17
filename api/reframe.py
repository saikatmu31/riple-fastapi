# api/reframe.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, PlainTextResponse
from models.request_models import ChatRequest
from services.llama_service import generate_reframed_prompt

router = APIRouter()

@router.post("/reframe")
async def reframe(request: ChatRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    if request.stream:
        return StreamingResponse(
            generate_reframed_prompt(request.prompt, request.max_tokens, request.temperature, request.stream),
            media_type="text/plain"
        )
    else:
        output = "".join(
            generate_reframed_prompt(request.prompt, request.max_tokens, request.temperature, request.stream)
        )
        return PlainTextResponse(output)
