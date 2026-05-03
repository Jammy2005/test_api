from pydantic import BaseModel

class InferenceRequest(BaseModel):
    """
    prompt: str
    max_tokens : int = 100
    """
    prompt: str
    max_tokens : int = 100


class InferenceResponse(BaseModel):
    """
    result: str
    tokens_used: int
    """
    result: str
    tokens_used: int