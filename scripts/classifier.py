from copy import deepcopy
import json
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

    def classify(
    self,
    article_name: str,
    instance_of: str = ""
    ):

        ####################################################
        # STEP 1 : ENTITY UNDERSTANDING
        ####################################################

        entity_prompt = self.entity_prompt_builder.build_prompt(
            article_name,
            instance_of
        )

        entity_profile = None

        for attempt in range(2):

            entity_response = self.model.generate(
                entity_prompt
            )

            try:

                entity_profile = JSONParser.parse(
                    entity_response
                )

                break

            except (json.JSONDecodeError, ValueError):

                if attempt == 1:
                    raise

                print(f"Attempt {attempt + 1}: Invalid JSON. Retrying...")

        ####################################################
        # CREATE CLEAN PROFILE FOR MAPPING
        ####################################################

        entity_for_mapping = deepcopy(
            entity_profile
        )

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

        ####################################################
        # STEP 3 : FINAL MCC SELECTION
        ####################################################

        mcc_prompt = self.mcc_prompt_builder.build_prompt(
            entity_for_mapping,
            candidates
        )

        final_result = None

        for attempt in range(2):

            mcc_response = self.model.generate(
                mcc_prompt
            )
            print("\n" + "=" * 80)
            print("RAW MCC RESPONSE")
            print("=" * 80)
            print(mcc_response)
            print("=" * 80 + "\n")

            try:

                final_result = JSONParser.parse(
                    mcc_response
                )
                print("\n" + "=" * 80)
                print("PARSED MCC RESULT")
                print("=" * 80)
                print(final_result)
                print("=" * 80 + "\n")

                break

            except json.JSONDecodeError:

                if attempt == 1:
                    raise

                print("Invalid JSON returned by model. Retrying...")

        ####################################################
        # STEP 4 : ADD CONFIDENCE TO TOP 5 MCCs
        ####################################################

        predictions = final_result.get(
            "top_5_mcc_predictions",
            []
        )

        if not predictions:

            raise ValueError(
                "Model did not return 'top_5_mcc_predictions'."
            )

        for prediction in predictions:

            selected_profile = None

            for profile in candidates:

                if str(profile["mcc"]) == str(
                    prediction.get("mcc")
                ):

                    selected_profile = profile
                    break

            if selected_profile is None:

                raise ValueError(
                    f"Model selected MCC "
                    f"{prediction.get('mcc')} "
                    f"which is not present in the retrieved candidates."
                )

            confidence = self.confidence.calculate(

                entity_profile=entity_profile,

                selected_profile=selected_profile

            )

            prediction["confidence"] = confidence

        ####################################################
        # RETURN
        ####################################################

        return {

            "entity_profile": entity_profile,

            "final_prediction": final_result

        }
