# api/embedding.py
from fastapi import APIRouter, HTTPException
from models.request_models import TextRequest
from services.embedding_service import generate_embedding

router = APIRouter()

@router.post("/embedding")
async def create_embedding(request: TextRequest):
    """
    Endpoint to generate an embedding for a given text.

    Args:
        request (TextRequest): Contains the text to be embedded and an optional boolean flag
            `extended` to indicate whether to return the expanded text.

    Returns:
        dict: A dictionary containing the following keys:
            - `success`: A boolean indicating whether the request was successful.
            - `message`: A string describing the result of the request.
            - `embedding`: The generated embedding as a list of floats. If the request was
                unsuccessful, this key is not present.
            - `expanded_text`: If `extended` is True, this key contains the expanded text
                after context expansion. If `extended` is False, this key is not present.
    """
    try:
        embedding, expanded_text = generate_embedding(request.text, request.extended)
        response = {
            "success": True,
            "message": "Embedding generated successfully",
            "embedding": embedding
        }
        if request.extended:
            response["expanded_text"] = expanded_text
        return response
    except HTTPException as http_ex:
        return {"success": False, "message": str(http_ex.detail), "embedding": None}
    except Exception as e:
        return {"success": False, "message": "Internal server error", "embedding": None}
