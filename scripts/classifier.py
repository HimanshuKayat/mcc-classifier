from models.llama_model import LlamaModel
from prompts.entity_prompt import EntityPromptBuilder
from prompts.mcc_prompt import MCCPromptBuilder
from retriever.embedding_retriever import EmbeddingRetriever
from semantic.agreement import ConfidenceScorer
from parser import JSONParser


class MCCClassifier:

    def __init__(self):

        self.model = LlamaModel()

        self.entity_prompt_builder = EntityPromptBuilder()

        self.mcc_prompt_builder = MCCPromptBuilder()

        self.retriever = EmbeddingRetriever()

        # Reuse the same embedding model already loaded
        self.confidence = ConfidenceScorer(
            self.retriever.model
        )

    def classify(self, page_name: str):

        ####################################################
        # STEP 1 : Entity Understanding
        ####################################################

        entity_prompt = self.entity_prompt_builder.build_prompt(page_name)

        entity_response = self.model.generate(entity_prompt)

        print("\n========== ENTITY UNDERSTANDING ==========\n")
        print(entity_response)
        print("\n==========================================\n")

        entity_profile = JSONParser.parse(entity_response)

        print("\n========== PARSED ENTITY PROFILE ==========\n")
        print(entity_profile)
        print("\n===========================================\n")

        ####################################################
        # SHOW MODEL'S INDEPENDENT MCC
        ####################################################

        print("\n========== MODEL'S INDEPENDENT MCC ==========\n")
        print(f"MCC       : {entity_profile.get('predicted_mcc','')}")
        print(f"Industry  : {entity_profile.get('predicted_mcc_industry','')}")
        print(f"Reason    : {entity_profile.get('predicted_mcc_reason','')}")
        print("\n============================================\n")

        ####################################################
        # STEP 2 : Retrieve Top MCC Candidates
        ####################################################

        candidates = self.retriever.retrieve(
            entity_profile,
            top_k=20
        )

        print("\n========== RETRIEVED MCC CANDIDATES ==========\n")

        for item in candidates:
            print(f"{item['mcc']} - {item['industry']}")

        print("\n=============================================\n")

        ####################################################
        # STEP 3 : Final MCC Selection
        ####################################################

        mcc_prompt = self.mcc_prompt_builder.build_prompt(
            entity_profile,
            candidates
        )

        mcc_response = self.model.generate(mcc_prompt)

        print("\n========== FINAL MCC RESPONSE ==========\n")
        print(mcc_response)
        print("\n========================================\n")

        final_result = JSONParser.parse(mcc_response)

        ####################################################
        # FIND SELECTED MCC PROFILE
        ####################################################

        selected_profile = None

        for profile in candidates:

            if profile["mcc"] == final_result["selected_mcc"]:
                selected_profile = profile
                break

        ####################################################
        # CALCULATE CONFIDENCE
        ####################################################

        if selected_profile is not None:

            confidence = self.confidence.calculate(
                entity_profile,
                selected_profile
            )

        else:

            confidence = 0.0

        final_result["confidence"] = confidence

        ####################################################
        # RETURN
        ####################################################

        return {

            "entity_profile": entity_profile,

            "final_prediction": final_result

        }
