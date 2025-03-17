from pydantic import BaseModel

class TextRequest(BaseModel):
    text: str
    extended: bool = False
    max_tokens: int = 100
    temperature: float = 0.3
    stream: bool = False
class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.3
    stream: bool = False