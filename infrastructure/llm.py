import asyncio

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential_jitter,  # exponential backoff + jitter combined
    retry_if_exception_type
)
import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

@retry(
    stop=stop_after_attempt(3),                    # max 3 attempts
    wait=wait_exponential_jitter(initial=1, max=8), # exponential backoff with jitter
    retry=retry_if_exception_type((TimeoutError, ConnectionError)) # only retry on transient errors
)
async def call_model(prompt: str, max_tokens: int):

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=max_tokens,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    tokens_generated = response.usage.output_tokens
    output_text = response.content[0].text

    return output_text, tokens_generated

# retry logic is far harder on streaming responses? do we want it only on initial connection setup? or with mid stream failure too? 
async def generate_tokens(prompt: str, max_tokens: int):
    # Use streaming mode
    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            yield f"data: {text}\n\n"  # send each token as it arrives
            # yield f"{text}"
    
    yield "data: [DONE]\n\n"

# async def test():
#     async for chunk in generate_tokens("How are you?", 300):
#         print(chunk)

# asyncio.run(test())