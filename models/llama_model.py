import requests


class LlamaModel:

    def __init__(
        self,
        model_name="llama3.1:8b",
        host="http://localhost:11434/api/generate"
    ):

        self.model_name = model_name
        self.host = host

    def generate(self, prompt: str) -> str:

        payload = {

            "model": self.model_name,

            "prompt": prompt,

            "stream": False,

            "format": "json",

            "options": {

                "temperature": 0,

                "num_predict": 1024

            }

        }

        response = requests.post(
            self.host,
            json=payload,
            timeout=300
        )

        if response.status_code != 200:

            raise Exception(
                f"Ollama Error {response.status_code}: {response.text}"
            )

        return response.json()["response"].strip()
