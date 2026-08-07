import pickle

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingRetriever:

    def __init__(
        self,
        embedding_file="data/mcc_embeddings.pkl",
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    ):

        # Load embedding model
        self.model = SentenceTransformer(
            model_name
        )

        # Load precomputed MCC embeddings
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
        # CREATE QUERY EMBEDDING
        ####################################################

        query_embedding = self.model.encode(

            [query],

            convert_to_numpy=True

        )

        ####################################################
        # COMPUTE COSINE SIMILARITY
        ####################################################

        similarities = cosine_similarity(

            query_embedding,

            self.embeddings

        )[0]

        ####################################################
        # SORT MCCs
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

        products = " | ".join(

            profile.get(
                "products_services",
                []
            )

        )

        customers = " | ".join(

            profile.get(
                "target_customers",
                []
            )

        )

        keywords = " | ".join(

            profile.get(
                "keywords",
                []
            )

        )

        aliases = " | ".join(

            profile.get(
                "aliases",
                []
            )

        )

        return f"""
Primary Business:
{profile.get("primary_business", "")}

Primary Business:
{profile.get("primary_business", "")}

Industry:
{profile.get("industry", "")}

Industry:
{profile.get("industry", "")}

Entity Type:
{profile.get("entity_type", "")}

Instance Of:
{profile.get("instance_of", "")}

Products and Services:
{products}

Products and Services:
{products}

Business Model:
{profile.get("business_model", "")}

Target Customers:
{customers}

Keywords:
{keywords}

Keywords:
{keywords}

Aliases:
{aliases}
"""
