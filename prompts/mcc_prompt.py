import json


class MCCPromptBuilder:

    def build_prompt(self, entity_profile, candidate_mccs):

        entity_json = json.dumps(
            entity_profile,
            indent=2,
            ensure_ascii=False
        )

        candidates = ""

        for i, item in enumerate(candidate_mccs, 1):

            candidates += (
                f"Rank: {i}\n"
                f"MCC: {item['mcc']}\n"
                f"Industry: {item['industry']}\n"
                f"Category: {item['category']}\n"
                f"Description: {item['description']}\n"
                f"Similarity: {item.get('retrieval_score', 0):.4f}\n"
                f"Keywords: {', '.join(item.get('keywords', []))}\n"
                "--------------------------------------------------\n"
            )

        return f"""
You are an expert Visa and Mastercard Merchant Category Code (MCC) classifier.

ENTITY

{entity_json}

TOP RETRIEVED MCC CANDIDATES

{candidates}

Task

Select the FIVE best MCCs.

Rules

- Use ONLY the candidates above.
- Never invent an MCC.
- Never repeat an MCC.
- Rank from best to worst semantic match.
- Prefer the merchant category that most closely represents the entity's primary commercial activity.
- If two candidates are similar, choose the more specific merchant category.
- Return ONLY valid JSON.

Output

{{
    "top_5_mcc_predictions": [
        {{
            "rank": 1,
            "mcc": "",
            "industry": "",
            "reason": ""
        }},
        {{
            "rank": 2,
            "mcc": "",
            "industry": "",
            "reason": ""
        }},
        {{
            "rank": 3,
            "mcc": "",
            "industry": "",
            "reason": ""
        }},
        {{
            "rank": 4,
            "mcc": "",
            "industry": "",
            "reason": ""
        }},
        {{
            "rank": 5,
            "mcc": "",
            "industry": "",
            "reason": ""
        }}
    ]
}}
"""
