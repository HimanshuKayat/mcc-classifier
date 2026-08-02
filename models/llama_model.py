import requests


class LlamaModel:

    def __init__(
        self,
        model_name="llama3.1:8b",
        host="http://localhost:11434/api/generate"
    ):
        self.model_name = model_name
        self.host = host

        print("\n==========================================")
        print("USING models/llama_model.py")
        print("==========================================\n")

    def generate(self, prompt: str) -> str:

        print("\n========== PROMPT SENT TO OLLAMA ==========\n")
        print(prompt)
        print("\n===========================================\n")

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(self.host, json=payload)

        if response.status_code != 200:
            raise Exception(
                f"Ollama Error {response.status_code}: {response.text}"
            )

        result = response.json()["response"].strip()

        print("\n========== RAW OLLAMA RESPONSE ==========\n")
        print(repr(result))
        print("\n=========================================\n")

        return result
