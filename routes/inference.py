from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from schemas.models import InferenceRequest, InferenceResponse
from services.model import run_inference, generate_tokens

router = APIRouter()

@router.post("/infer", response_model=InferenceResponse)
async def infer(request: InferenceRequest):
    
    # NEED TO ADD ERROR HANDLING
    prompt = request.prompt
    max_tokens = request.max_tokens

    result, tokens_used = await run_inference(prompt, max_tokens)

    print (f"DEBUG: {(result)}, {type(tokens_used)}")
    response = InferenceResponse(
        result = result,
        tokens_used = tokens_used
    )
    print(f"printing the type of RESPONSE in the inference.py: {type(response)}")
    return response

@router.post("/infer/stream", response_model=InferenceResponse)
async def infer_stream(request: InferenceRequest):
    
    return StreamingResponse(
        generate_tokens(request.prompt, request.max_tokens),
        media_type="text/event-stream"
        )



