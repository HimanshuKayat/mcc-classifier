import pickle
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingRetriever:

    def __init__(
        self,
        embedding_file="data/mcc_embeddings.pkl",
        model_name="BAAI/bge-large-en-v1.5"
    ):

        self.model = SentenceTransformer(model_name)

        with open(embedding_file, "rb") as f:
            data = pickle.load(f)

        self.mcc_profiles = data["profiles"]
        self.embeddings = data["embeddings"]

    ####################################################
    # PUBLIC
    ####################################################

    def retrieve(
        self,
        entity_profile,
        top_k=20
    ):

        query = self._profile_to_text(
            entity_profile
        )

        embedding = self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        scores = cosine_similarity(
            [embedding],
            self.embeddings
        )[0]

        indices = np.argsort(scores)[::-1][:top_k]

        results = []

        for idx in indices:

            profile = self.mcc_profiles[idx].copy()

            profile["retrieval_score"] = round(
                float(scores[idx]),
                4
            )

            results.append(profile)

        return results

    ####################################################
    # QUERY REPRESENTATION
    ####################################################

    def _profile_to_text(
        self,
        profile
    ):

        fields = [

            profile.get(
                "entity_type",
                ""
            ),

            profile.get(
                "primary_business",
                ""
            ),

            profile.get(
                "industry",
                ""
            ),

            ", ".join(
                profile.get(
                    "products_services",
                    []
                )
            ),

            ", ".join(
                profile.get(
                    "target_customers",
                    []
                )
            ),

            profile.get(
                "country",
                ""
            ),

            ", ".join(
                profile.get(
                    "keywords",
                    []
                )
            ),

            ", ".join(
                profile.get(
                    "aliases",
                    []
                )
            )

        ]

        return " | ".join(

            field.strip()

            for field in fields

            if field and field.strip()

        )
