from sklearn.metrics.pairwise import cosine_similarity


class ConfidenceScorer:

    def __init__(self, embedding_model):
        self.model = embedding_model

    def _encode_similarity(self, text1, text2):

        if not text1.strip() or not text2.strip():
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

    def _entity_profile(self, entity):

        return f"""
Entity Name:
{entity.get("entity_name","")}

Entity Type:
{entity.get("entity_type","")}

Summary:
{entity.get("summary","")}

Primary Business:
{entity.get("primary_business","")}

Industry:
{entity.get("industry","")}

Products:
{' '.join(entity.get("products_services", []))}

Target Customers:
{' '.join(entity.get("target_customers", []))}

Business Model:
{entity.get("business_model","")}

Keywords:
{' '.join(entity.get("keywords", []))}

Aliases:
{' '.join(entity.get("aliases", []))}
"""

    def _mcc_profile(self, mcc):

        return f"""
MCC:
{mcc.get("mcc","")}

Industry:
{mcc.get("industry","")}

Category:
{mcc.get("category","")}

Description:
{mcc.get("description","")}

Keywords:
{' '.join(mcc.get("keywords", []))}

Aliases:
{' '.join(mcc.get("aliases", []))}
"""

    def calculate(self, entity_profile, selected_profile):

        entity_text = self._entity_profile(entity_profile)

        mcc_text = self._mcc_profile(selected_profile)

        semantic_similarity = self._encode_similarity(
            entity_text,
            mcc_text
        )

        retrieval_similarity = selected_profile.get(
            "retrieval_score",
            semantic_similarity
        )

        confidence = (
            semantic_similarity * 0.70 +
            retrieval_similarity * 0.30
        ) * 100

        confidence = max(0.0, min(100.0, confidence))

        return round(confidence, 2)
