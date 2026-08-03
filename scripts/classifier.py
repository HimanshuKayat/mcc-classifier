from models.llama_model import LlamaModel
from prompts.prompt_builder import PromptBuilder
from parser import JSONParser


class MCCClassifier:

    def __init__(self):
        self.model = LlamaModel()
        self.prompt_builder = PromptBuilder()

    def classify(self, page_name: str):

        prompt = self.prompt_builder.build_prompt(page_name)

        response = self.model.generate(prompt)

        print("\n========== RAW LLM RESPONSE ==========\n")
        print(repr(response))
        print("\n======================================\n")

        result = JSONParser.parse(response)

        return result
