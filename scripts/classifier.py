from copy import deepcopy

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

        self.confidence = ConfidenceScorer(
            self.retriever.model
        )

    def classify(self, page_name: str):

        ####################################################
        # STEP 1 : ENTITY UNDERSTANDING
        ####################################################

        entity_prompt = self.entity_prompt_builder.build_prompt(
            page_name
        )

        entity_response = self.model.generate(
            entity_prompt
        )

        print("\n========== ENTITY UNDERSTANDING ==========\n")
        print(entity_response)
        print("\n==========================================\n")

        entity_profile = JSONParser.parse(
            entity_response
        )

        print("\n========== PARSED ENTITY PROFILE ==========\n")
        print(entity_profile)
        print("\n===========================================\n")

        ####################################################
        # MODEL'S INDEPENDENT MCC
        ####################################################

        if entity_profile.get("predicted_mcc"):

            print("\n========== MODEL'S INDEPENDENT MCC ==========\n")

            print(
                f"MCC       : {entity_profile.get('predicted_mcc','')}"
            )

            print(
                f"Industry  : {entity_profile.get('predicted_mcc_industry','')}"
            )

            print(
                f"Reason    : {entity_profile.get('predicted_mcc_reason','')}"
            )

            print("\n============================================\n")

        ####################################################
        # CREATE CLEAN PROFILE FOR MAPPING
        ####################################################

        entity_for_mapping = deepcopy(entity_profile)

        entity_for_mapping.pop(
            "predicted_mcc",
            None
        )

        entity_for_mapping.pop(
            "predicted_mcc_industry",
            None
        )

        entity_for_mapping.pop(
            "predicted_mcc_reason",
            None
        )

        ####################################################
        # STEP 2 : RETRIEVE MCC CANDIDATES
        ####################################################

        candidates = self.retriever.retrieve(
            entity_for_mapping,
            top_k=20
        )

        print("\n========== RETRIEVED MCC CANDIDATES ==========\n")

        for item in candidates:

            print(
                f"{item['mcc']} - {item['industry']}"
            )

        print("\n=============================================\n")

        ####################################################
        # STEP 3 : FINAL MCC SELECTION
        ####################################################

        mcc_prompt = self.mcc_prompt_builder.build_prompt(
            entity_for_mapping,
            candidates
        )

        mcc_response = self.model.generate(
            mcc_prompt
        )

        print("\n========== FINAL MCC RESPONSE ==========\n")
        print(mcc_response)
        print("\n========================================\n")

        final_result = JSONParser.parse(
            mcc_response
        )

        ####################################################
        # FIND SELECTED PROFILE
        ####################################################

        selected_profile = None

        for profile in candidates:

            if str(profile["mcc"]) == str(
                final_result.get("selected_mcc")
            ):

                selected_profile = profile
                break

        ####################################################
        # INVALID MCC
        ####################################################

        if selected_profile is None:

            raise ValueError(
                f"\nModel selected MCC "
                f"{final_result.get('selected_mcc')} "
                f"which is not present in the retrieved candidates."
            )

        ####################################################
        # STEP 4 : CONFIDENCE
        ####################################################

        confidence = self.confidence.calculate(

            entity_profile=entity_profile,

            selected_profile=selected_profile

        )

        final_result["confidence"] = confidence

        print("\n========== CONFIDENCE ==========\n")
        print(f"Confidence : {confidence}%")
        print("\n================================\n")

        ####################################################
        # RETURN
        ####################################################

        return {

            "entity_profile": entity_profile,

            "final_prediction": final_result

        }
