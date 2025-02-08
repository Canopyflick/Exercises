# utils/streaming.py
import os
import asyncio
from huggingface_hub import AsyncInferenceClient


async def stream_chat_completion(messages, model_name: str, max_tokens: int = 1024):
    """
    Stream tokens from a Hugging Face Inference endpoint.

    Args:
        messages (list[dict]): A list of message dictionaries, e.g.:
            [{"role": "system", "content": "You are a helpful assistant."},
             {"role": "user", "content": "Count to 10"}]
        model_name (str): The identifier for the model (used in the base_url).
        max_tokens (int): Maximum tokens to generate.

    Yields:
        str: Tokens as they are generated.
    """
    # Construct a base URL that points to the model’s endpoint.
    base_url = f"https://api-inference.huggingface.co/models/{model_name}"
    token = os.getenv("HF_API_TOKEN")
    client = AsyncInferenceClient(base_url=base_url, token=token)

    stream = await client.chat.completions.create(
        messages=messages,
        stream=True,
        max_tokens=max_tokens,
    )

    async for chunk in stream:
        # Each chunk is expected to have a structure where the generated text is in:
        # chunk.choices[0].delta.content
        yield chunk.choices[0].delta.content or ""
