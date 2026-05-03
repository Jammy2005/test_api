import asyncio
from infrastructure.llm import call_model, generate_tokens

# mimicks an actual model being called or an agent being invoked
async def run_inference(prompt: str, max_tokens: int = 100):

    # await asyncio.sleep(3) # emulating infernce time

    output_text, tokens_generated = await call_model(prompt, max_tokens)

    return output_text, tokens_generated

# can test business logic independently
# result = asyncio.run(run_inference("How are you?", 300))
# print(result)
    
async def stream_inference(prompt: str, max_tokens: int = 100):

    async for chunk in generate_tokens(prompt, max_tokens):
        
        yield chunk
