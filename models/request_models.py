from pydantic import BaseModel

class TextRequests(BaseModel):
    text: str
    extended: bool = False
    max_tokens: int = 100
    temperature: float = 0.3
    stream: bool = False
