from models.ollama_model import OllamaModel
from prompts.prompt_builder import PromptBuilder
from parser import JSONParser


class MCCClassifier:

    def __init__(self):
        self.model = OllamaModel()
        self.prompt_builder = PromptBuilder()

    def classify(self, page_name):

        prompt = self.prompt_builder.build_prompt(page_name)

        response = self.model.generate(prompt)

        print("\n========== RAW MODEL RESPONSE ==========\n")
        print(response)
        print("\n========================================\n")

        return JSONParser.parse(response)
