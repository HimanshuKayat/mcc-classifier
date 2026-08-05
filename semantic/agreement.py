from sklearn.metrics.pairwise import cosine_similarity


class ConfidenceScorer:

    def __init__(self, embedding_model):
        self.model = embedding_model

    def _similarity(self, text1, text2):

        if not text1 or not text2:
            return 0.0

        embeddings = self.model.encode(
            [text1, text2],
            convert_to_numpy=True
        )

        return float(
            cosine_similarity(
                [embeddings[0]],
                [embeddings[1]]
            )[0][0]
        )

    def calculate(
        self,
        entity_profile,
        selected_profile
    ):

        business_similarity = self._similarity(
            entity_profile.get("primary_business", ""),
            selected_profile.get("description", "")
        )

        industry_similarity = self._similarity(
            entity_profile.get("industry", ""),
            selected_profile.get("industry", "")
        )

        reason_similarity = self._similarity(
            entity_profile.get("predicted_mcc_reason", ""),
            selected_profile.get("description", "")
        )

        confidence = (
            business_similarity * 0.40 +
            industry_similarity * 0.35 +
            reason_similarity * 0.25
        ) * 100

        confidence = max(0, min(100, confidence))

        return round(confidence, 2)
