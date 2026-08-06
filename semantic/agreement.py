from sklearn.metrics.pairwise import cosine_similarity


class ConfidenceScorer:

    def __init__(self, embedding_model):

        self.model = embedding_model

    def _similarity(self, text1, text2):

        if not text1.strip() or not text2.strip():
            return 0.0

        embeddings = self.model.encode(
            [text1, text2],
            convert_to_numpy=True
        )

        similarity = cosine_similarity(
            [embeddings[0]],
            [embeddings[1]]
        )[0][0]

        return float(similarity)

    #########################################################
    # MODEL'S PREDICTED MCC PROFILE
    #########################################################

    def _predicted_profile(self, entity):

        return f"""
Entity Name:
{entity.get("entity_name","")}

Entity Type:
{entity.get("entity_type","")}

Primary Business:
{entity.get("primary_business","")}

Industry:
{entity.get("industry","")}

Predicted MCC:
{entity.get("predicted_mcc","")}

Predicted MCC Industry:
{entity.get("predicted_mcc_industry","")}

Predicted Reason:
{entity.get("predicted_mcc_reason","")}
"""

    #########################################################
    # RETRIEVED / FINAL MCC PROFILE
    #########################################################

    def _selected_profile(self, profile):

        return f"""
MCC:
{profile.get("mcc","")}

Industry:
{profile.get("industry","")}

Category:
{profile.get("category","")}

Description:
{profile.get("description","")}

Keywords:
{' '.join(profile.get("keywords", []))}

Aliases:
{' '.join(profile.get("aliases", []))}
"""

    #########################################################
    # FINAL CONFIDENCE
    #########################################################

    def calculate(
        self,
        entity_profile,
        selected_profile
    ):

        predicted_text = self._predicted_profile(
            entity_profile
        )

        selected_text = self._selected_profile(
            selected_profile
        )

        semantic_similarity = self._similarity(
            predicted_text,
            selected_text
        )

        retrieval_similarity = float(
            selected_profile.get(
                "retrieval_score",
                0.0
            )
        )

        confidence = (

            semantic_similarity * 0.80 +

            retrieval_similarity * 0.20

        ) * 100

        confidence = max(
            0,
            min(
                confidence,
                100
            )
        )

        return round(confidence, 2)
