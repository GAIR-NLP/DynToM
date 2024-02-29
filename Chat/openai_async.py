import httpx

def _send_to_openai(endpoint_url: str,):
    async def send_to_openai(api_key: str, timeout: float, payload: dict) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            return await client.post(
                url=endpoint_url,
                json=payload,
                headers={"content_type": "application/json", "Authorization": f"Bearer {api_key}"},
                timeout=timeout,
            )

    return send_to_openai

api_base = "https://lonlie.plus7.plus/v1"
complete = _send_to_openai(f"{api_base}/completions")
generate_img = _send_to_openai(f"{api_base}/images/generations")
embeddings = _send_to_openai(f"{api_base}/embeddings")
chat_complete = _send_to_openai(f"{api_base}/chat/completions")
