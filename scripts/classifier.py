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
        # MODEL'S INDEPENDENT MCC (Optional)
        ####################################################

        if entity_profile.get("predicted_mcc"):

            print("\n========== MODEL'S INDEPENDENT MCC ==========\n")
            print(f"MCC       : {entity_profile.get('predicted_mcc','')}")
            print(f"Industry  : {entity_profile.get('predicted_mcc_industry','')}")
            print(f"Reason    : {entity_profile.get('predicted_mcc_reason','')}")
            print("\n============================================\n")

        ####################################################
        # STEP 2 : RETRIEVE TOP MCC CANDIDATES
        ####################################################

        candidates = self.retriever.retrieve(
            entity_profile,
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
            entity_profile,
            candidates
        )

        mcc_response = self.model.generate(mcc_prompt)

        print("\n========== FINAL MCC RESPONSE ==========\n")
        print(mcc_response)
        print("\n========================================\n")

        final_result = JSONParser.parse(mcc_response)

        ####################################################
        # VALIDATE SELECTED MCC
        ####################################################

        candidate_lookup = {
            str(profile["mcc"]): profile
            for profile in candidates
        }

        selected_profile = candidate_lookup.get(
            str(final_result.get("selected_mcc", ""))
        )

        if selected_profile is None:

            print("\nWARNING")
            print("=" * 60)
            print("Model selected an MCC outside the retrieved candidates.")
            print(f"Returned MCC : {final_result.get('selected_mcc')}")
            print("Automatically selecting highest-ranked retrieved MCC.")
            print("=" * 60)

            selected_profile = candidates[0]

            final_result["selected_mcc"] = selected_profile["mcc"]
            final_result["selected_industry"] = selected_profile["industry"]

            final_result["selected_reason"] = (
                "Model returned an MCC outside the retrieved candidate list. "
                "Highest-ranked retrieved MCC selected automatically."
            )

        ####################################################
        # STEP 4 : CALCULATE CONFIDENCE
        ####################################################

        confidence = self.confidence.calculate(
            entity_profile,
            selected_profile
        )

        final_result["confidence"] = confidence

        print("\n========== CONFIDENCE DEBUG ==========\n")
        print(
            f"Retriever Score : {selected_profile.get('retrieval_score', 0):.4f}"
        )
        print(f"Confidence      : {confidence}%")
        print("\n======================================\n")

        ####################################################
        # RETURN
        ####################################################

        return {
            "entity_profile": entity_profile,
            "final_prediction": final_result
        }
