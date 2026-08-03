import requests


class OllamaModel:
    def __init__(
        self,
        model_name="qwen3:8b",
        host="http://localhost:11434/api/generate",
        timeout=300,
    ):
        self.model_name = model_name
        self.host = host
        self.timeout = timeout

    def generate(self, prompt: str) -> str:

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
        }

        response = requests.post(
            self.host,
            json=payload,
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()["response"].strip()
