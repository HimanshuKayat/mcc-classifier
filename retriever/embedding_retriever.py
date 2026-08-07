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

    def retrieve(
        self,
        entity_profile,
        top_k=20
    ):

        query = self._profile_to_text(
            entity_profile
        )

        query_embedding = self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        similarities = cosine_similarity(
            [query_embedding],
            self.embeddings
        )[0]

        top_indices = np.argsort(
            similarities
        )[::-1][:top_k]

        results = []

        for idx in top_indices:

            profile = self.mcc_profiles[idx].copy()

            profile["retrieval_score"] = float(
                similarities[idx]
            )

            results.append(profile)

        return results

    def _profile_to_text(
        self,
        profile
    ):

        entity_type = profile.get(
            "entity_type",
            ""
        )

        business = profile.get(
            "primary_business",
            ""
        )

        industry = profile.get(
            "industry",
            ""
        )

        country = profile.get(
            "country",
            ""
        )

        products = ", ".join(
            profile.get(
                "products_services",
                []
            )
        )

        customers = ", ".join(
            profile.get(
                "target_customers",
                []
            )
        )

        keywords = ", ".join(
            profile.get(
                "keywords",
                []
            )
        )

        aliases = ", ".join(
            profile.get(
                "aliases",
                []
            )
        )

        return (
            f"Entity: {entity_type}. "
            f"Business: {business}. "
            f"Industry: {industry}. "
            f"Products: {products}. "
            f"Customers: {customers}. "
            f"Country: {country}. "
            f"Keywords: {keywords}. "
            f"Aliases: {aliases}."
        )
