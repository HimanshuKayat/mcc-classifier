from models.llama_model import LlamaModel
from prompts.entity_prompt import EntityPromptBuilder
from prompts.mcc_prompt import MCCPromptBuilder
from parser import JSONParser


class MCCClassifier:

    def __init__(self):

        self.model = LlamaModel()

        self.entity_prompt_builder = EntityPromptBuilder()

        self.mcc_prompt_builder = MCCPromptBuilder()

    def classify(self, page_name: str):

        ####################################################
        # STEP 1 : Understand the Wikipedia Article
        ####################################################

        entity_prompt = self.entity_prompt_builder.build_prompt(page_name)

        entity_response = self.model.generate(entity_prompt)

        print("\n========== ENTITY UNDERSTANDING ==========\n")
        print(entity_response)
        print("\n==========================================\n")

        entity_profile = JSONParser.parse(entity_response)

        ####################################################
        # STEP 2 : Map Business Profile to MCC
        ####################################################

        mcc_prompt = self.mcc_prompt_builder.build_prompt(entity_profile)

        mcc_response = self.model.generate(mcc_prompt)

        print("\n========== MCC MAPPING ==========\n")
        print(mcc_response)
        print("\n=================================\n")

        result = JSONParser.parse(mcc_response)

        return result
