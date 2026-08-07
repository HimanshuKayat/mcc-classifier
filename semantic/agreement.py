from sklearn.metrics.pairwise import cosine_similarity


class ConfidenceScorer:

    def __init__(self, embedding_model):

        self.model = embedding_model

    ####################################################
    # EMBEDDING SIMILARITY
    ####################################################

    def _similarity(

        self,

        text1,

        text2

    ):

        if not text1.strip() or not text2.strip():

            return 0.0

        embeddings = self.model.encode(

            [text1, text2],

            convert_to_numpy=True,

            normalize_embeddings=True

        )

        similarity = cosine_similarity(

            [embeddings[0]],

            [embeddings[1]]

        )[0][0]

        return float(similarity)

    ####################################################
    # ENTITY REPRESENTATION
    ####################################################

    def _entity_text(

        self,

        entity

    ):

        return (
            f"{entity.get('entity_type','')} | "
            f"{entity.get('primary_business','')} | "
            f"{entity.get('industry','')} | "
            f"{' '.join(entity.get('products_services', []))} | "
            f"{' '.join(entity.get('keywords', []))} | "
            f"{' '.join(entity.get('aliases', []))}"
        )

    ####################################################
    # MCC REPRESENTATION
    ####################################################

    def _mcc_text(

        self,

        profile

    ):

        return (
            f"{profile.get('industry','')} | "
            f"{profile.get('category','')} | "
            f"{profile.get('description','')} | "
            f"{' '.join(profile.get('keywords', []))} | "
            f"{' '.join(profile.get('aliases', []))}"
        )

    ####################################################
    # FINAL CONFIDENCE
    ####################################################

    def calculate(

        self,

        entity_profile,

        selected_profile

    ):

        semantic_similarity = self._similarity(

            self._entity_text(entity_profile),

            self._mcc_text(selected_profile)

        )

        retrieval_similarity = float(

            selected_profile.get(

                "retrieval_score",

                0.0

            )

        )

        confidence = (

            semantic_similarity * 0.70 +

            retrieval_similarity * 0.30

        ) * 100

        confidence = max(

            0,

            min(

                confidence,

                100

            )

        )

        return round(confidence, 2)
