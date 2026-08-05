from sklearn.metrics.pairwise import cosine_similarity


class ConfidenceScorer:

    def __init__(self, embedding_model):

        self.model = embedding_model

    def _similarity(self, text1, text2):

        text1 = str(text1).strip()
        text2 = str(text2).strip()

        if not text1 or not text2:
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

    def calculate(
        self,
        entity_profile,
        selected_profile
    ):

        ##################################################
        # MODEL'S INDEPENDENT UNDERSTANDING
        ##################################################

        predicted_industry = entity_profile.get(
            "predicted_mcc_industry",
            ""
        )

        predicted_reason = entity_profile.get(
            "predicted_mcc_reason",
            ""
        )

        ##################################################
        # FINAL MAPPED MCC
        ##################################################

        selected_industry = selected_profile.get(
            "industry",
            ""
        )

        selected_description = selected_profile.get(
            "description",
            ""
        )

        ##################################################
        # SEMANTIC AGREEMENT
        ##################################################

        industry_similarity = self._similarity(

            predicted_industry,

            selected_industry

        )

        reason_similarity = self._similarity(

            predicted_reason,

            selected_description

        )

        retrieval_similarity = float(

            selected_profile.get(
                "retrieval_score",
                0.0
            )

        )

        ##################################################
        # FINAL CONFIDENCE
        ##################################################

        confidence = (

            industry_similarity * 0.40 +

            reason_similarity * 0.40 +

            retrieval_similarity * 0.20

        ) * 100

        confidence = max(
            0.0,
            min(
                confidence,
                100.0
            )
        )

        ##################################################
        # DEBUG
        ##################################################

        print("\n========== CONFIDENCE BREAKDOWN ==========\n")

        print(
            f"Industry Similarity : {industry_similarity:.3f}"
        )

        print(
            f"Reason Similarity   : {reason_similarity:.3f}"
        )

        print(
            f"Retriever Score     : {retrieval_similarity:.3f}"
        )

        print(
            f"Final Confidence    : {confidence:.2f}%"
        )

        print("\n==========================================\n")

        return round(confidence, 2)
