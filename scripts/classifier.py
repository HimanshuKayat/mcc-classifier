from models.llama_model import LlamaModel
from prompts.prompt_builder import PromptBuilder
from parser import JSONParser


class MCCClassifier:

    def __init__(self):
        self.model = LlamaModel()
        self.prompt_builder = PromptBuilder()

    def classify(self, page_name: str):

        # Build prompt
        prompt = self.prompt_builder.build_prompt(page_name)

        # Generate response
        response = self.model.generate(prompt)

        print("\n========== RAW LLM RESPONSE ==========\n")
        print(repr(response))
        print("\n======================================\n")

        # Parse JSON
        result = JSONParser.parse(response)

        return result
