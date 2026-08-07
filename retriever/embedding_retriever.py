import pickle

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingRetriever:

    def __init__(
        self,
        embedding_file="data/mcc_embeddings.pkl",
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    ):

        self.model = SentenceTransformer(
            model_name
        )

        with open(
            embedding_file,
            "rb"
        ) as f:

            data = pickle.load(f)

        self.mcc_profiles = data["profiles"]

        self.embeddings = data["embeddings"]

    def retrieve(
        self,
        entity_profile,
        top_k=20
    ):

        ####################################################
        # BUILD QUERY
        ####################################################

        query = self._profile_to_text(
            entity_profile
        )

        ####################################################
        # CREATE EMBEDDING
        ####################################################

        query_embedding = self.model.encode(

            [query],

            convert_to_numpy=True

        )

        ####################################################
        # COSINE SIMILARITY
        ####################################################

        similarities = cosine_similarity(

            query_embedding,

            self.embeddings

        )[0]

        ####################################################
        # SORT
        ####################################################

        ranked = sorted(

            zip(
                similarities,
                self.mcc_profiles
            ),

            key=lambda x: x[0],

            reverse=True

        )

        ####################################################
        # RETURN TOP K
        ####################################################

        results = []

        for similarity, profile in ranked[:top_k]:

            profile_copy = profile.copy()

            profile_copy["retrieval_score"] = float(
                similarity
            )

            results.append(
                profile_copy
            )

        return results

    def _profile_to_text(
        self,
        profile
    ):

        primary_business = profile.get(
            "primary_business",
            ""
        )

        industry = profile.get(
            "industry",
            ""
        )

        entity_type = profile.get(
            "entity_type",
            ""
        )

        instance_of = profile.get(
            "instance_of",
            ""
        )

        products = " ".join(

            profile.get(
                "products_services",
                []
            )

        )

        keywords = " ".join(

            profile.get(
                "keywords",
                []
            )

        )

        return (
            f"{primary_business}. "
            f"{industry}. "
            f"{entity_type}. "
            f"{instance_of}. "
            f"{products}. "
            f"{keywords}."
        )
