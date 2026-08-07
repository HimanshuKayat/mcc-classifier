import pickle
import re
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
    # MAIN RETRIEVAL
    ####################################################

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

        ####################################################
        # GET TOP 60 BY EMBEDDINGS
        ####################################################

        candidate_indices = np.argsort(
            similarities
        )[::-1][:60]

        ####################################################
        # RERANK
        ####################################################

        ranked = []

        for idx in candidate_indices:

            profile = self.mcc_profiles[idx].copy()

            embedding_score = float(
                similarities[idx]
            )

            keyword_bonus = self._keyword_bonus(
                entity_profile,
                profile
            )

            industry_bonus = self._industry_bonus(
                entity_profile,
                profile
            )

            final_score = (
                embedding_score +
                keyword_bonus +
                industry_bonus
            )

            profile["retrieval_score"] = round(
                final_score,
                4
            )

            ranked.append(profile)

        ranked.sort(

            key=lambda x: x["retrieval_score"],

            reverse=True

        )

        return ranked[:top_k]

    ####################################################
    # QUERY REPRESENTATION
    ####################################################

    def _profile_to_text(
        self,
        profile
    ):

        return (
            f"Entity: {profile.get('entity_type','')}. "
            f"Business: {profile.get('primary_business','')}. "
            f"Industry: {profile.get('industry','')}. "
            f"Products: {', '.join(profile.get('products_services', []))}. "
            f"Customers: {', '.join(profile.get('target_customers', []))}. "
            f"Country: {profile.get('country','')}. "
            f"Keywords: {', '.join(profile.get('keywords', []))}. "
            f"Aliases: {', '.join(profile.get('aliases', []))}."
        )

    ####################################################
    # TOKENIZER
    ####################################################

    def _tokens(self, text):

        return {

            token

            for token in re.findall(

                r"[a-zA-Z0-9]+",

                text.lower()

            )

            if len(token) > 2

        }

    ####################################################
    # KEYWORD BONUS
    ####################################################

    def _keyword_bonus(

        self,

        entity,

        mcc

    ):

        entity_tokens = set()

        entity_tokens |= self._tokens(

            entity.get(

                "primary_business",

                ""

            )

        )

        entity_tokens |= self._tokens(

            entity.get(

                "industry",

                ""

            )

        )

        entity_tokens |= {

            x.lower()

            for x in entity.get(

                "keywords",

                []

            )

        }

        mcc_tokens = set()

        mcc_tokens |= self._tokens(

            mcc.get(

                "industry",

                ""

            )

        )

        mcc_tokens |= self._tokens(

            mcc.get(

                "category",

                ""

            )

        )

        mcc_tokens |= self._tokens(

            mcc.get(

                "description",

                ""

            )

        )

        mcc_tokens |= {

            x.lower()

            for x in mcc.get(

                "keywords",

                []

            )

        }

        overlap = len(

            entity_tokens & mcc_tokens

        )

        return min(

            overlap * 0.02,

            0.10

        )

    ####################################################
    # INDUSTRY BONUS
    ####################################################

    def _industry_bonus(

        self,

        entity,

        mcc

    ):

        entity_industry = entity.get(

            "industry",

            ""

        ).lower()

        mcc_industry = mcc.get(

            "industry",

            ""

        ).lower()

        if not entity_industry:

            return 0.0

        if entity_industry == mcc_industry:

            return 0.08

        if entity_industry in mcc_industry:

            return 0.05

        if mcc_industry in entity_industry:

            return 0.05

        return 0.0
