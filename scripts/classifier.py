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

    ####################################################
    # MAIN
    ####################################################

    def classify(
        self,
        article_name: str,
        instance_of: str = ""
    ):

        ####################################################
        # ENTITY EXTRACTION
        ####################################################

        entity_prompt = self.entity_prompt_builder.build_prompt(

            article_name,

            instance_of

        )

        entity_response = self.model.generate(

            entity_prompt

        )

        entity_profile = JSONParser.parse(

            entity_response

        )

        ####################################################
        # CLEAN PROFILE
        ####################################################

        entity_for_mapping = {

            k: v

            for k, v in entity_profile.items()

            if not k.startswith("predicted_")

        }

        ####################################################
        # RETRIEVE MCCs
        ####################################################

        candidates = self.retriever.retrieve(

            entity_for_mapping,

            top_k=20

        )

        ####################################################
        # FAST LOOKUP
        ####################################################

        candidate_lookup = {

            str(c["mcc"]): c

            for c in candidates

        }

        ####################################################
        # FINAL PROMPT
        ####################################################

        mcc_prompt = self.mcc_prompt_builder.build_prompt(

            entity_for_mapping,

            candidates

        )

        mcc_response = self.model.generate(

            mcc_prompt

        )

        final_result = JSONParser.parse(

            mcc_response

        )

        ####################################################
        # VALIDATE
        ####################################################

        predictions = final_result.get(

            "top_5_mcc_predictions",

            []

        )

        if len(predictions) != 5:

            raise ValueError(
                f"Expected 5 MCC predictions, got {len(predictions)}."
            )

        ####################################################
        # CONFIDENCE
        ####################################################

        used_mccs = set()

        for prediction in predictions:

            mcc = str(
                prediction.get(
                    "mcc",
                    ""
                )
            )

            if mcc in used_mccs:

                raise ValueError(
                    f"Duplicate MCC returned: {mcc}"
                )

            used_mccs.add(mcc)

            if mcc not in candidate_lookup:

                raise ValueError(
                    f"MCC {mcc} was not retrieved."
                )

            selected_profile = candidate_lookup[mcc]

            confidence = self.confidence.calculate(

                entity_profile=entity_profile,

                selected_profile=selected_profile

            )

            prediction["confidence"] = confidence

            prediction["retrieval_score"] = round(

                selected_profile.get(
                    "retrieval_score",
                    0.0
                ),

                4

            )

        ####################################################
        # SORT BY RANK
        ####################################################

        predictions.sort(

            key=lambda x: x.get(
                "rank",
                999
            )

        )

        ####################################################
        # RETURN
        ####################################################

        return {

            "entity_profile": entity_profile,

            "final_prediction": {

                "top_5_mcc_predictions": predictions

            }

        }
