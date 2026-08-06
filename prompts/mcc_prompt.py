import json


class MCCPromptBuilder:

    def build_prompt(self, entity_profile, candidate_mccs):

        entity_json = json.dumps(
            entity_profile,
            indent=4,
            ensure_ascii=False
        )

        mcc_text = ""

        for item in candidate_mccs:

            mcc_text += (
                f"MCC: {item.get('mcc', '')}\n"
                f"Industry: {item.get('industry', '')}\n"
                f"Category: {item.get('category', '')}\n"
                f"Description: {item.get('description', '')}\n"
                f"Keywords: {', '.join(item.get('keywords', []))}\n"
                f"Aliases: {', '.join(item.get('aliases', []))}\n"
                "------------------------------------------------------------\n"
            )

        prompt = f"""
You are an expert Merchant Category Code (MCC) classifier.

========================================================
STAGE 1 BUSINESS PROFILE
========================================================

Below is the structured business profile generated from Stage 1.

{entity_json}

========================================================
RETRIEVED MCC CANDIDATES
========================================================

Below are the ONLY MCCs you are allowed to choose from.

{mcc_text}

========================================================
YOUR TASK
========================================================

Your objective is NOT to find matching keywords.

Your objective is to determine the real-world merchant activity, commercial transaction, or business intent represented by the entity, and then identify the MCCs whose business profiles are semantically the closest match.

Reason using semantic meaning, not word overlap.

GUIDELINES

• Companies:
  Focus on the primary revenue-generating business, products/services, business model, and what customers pay for.

• Products:
  Focus on the merchant category through which the product is typically sold.

• Places:
  Focus on the dominant commercial activity occurring at that place (tourism, hospitality, transportation, retail, etc.).

• People:
  Do NOT classify the person themselves.
  Instead, infer the most likely commercial interest or transaction associated with that person.
  Examples include movies, music, books, sports, education, digital content, travel, merchandise, etc.

• Movies, TV Shows, Games, Books, Events:
  Focus on how consumers access or purchase them (streaming, cinemas, digital media, tickets, bookstores, gaming platforms, etc.).

COMPARISON PROCESS

1. Understand the entity's primary commercial activity.
2. Compare EVERY retrieved MCC candidate semantically.
3. Evaluate Industry, Description, Category, Keywords, Business Activity, and Customer Transaction.
4. Identify the FIVE strongest semantic matches.
5. Order these five from the strongest semantic match to the fifth strongest semantic match.
6. The MCC ranked first should be the same MCC you would select if asked to return only one MCC.
7. Do NOT choose an MCC because it shares similar words with the entity.
8. If multiple candidates appear similar, rank them according to how closely their overall business model and customer transaction match the entity.

CRITICAL RULES

1. You MUST return EXACTLY FIVE MCCs.
2. These MUST be the FIVE strongest semantic matches from the retrieved candidate list.
3. Every MCC MUST exist in the retrieved candidate list.
4. Never invent an MCC.
5. Never use an MCC outside the retrieved candidates.
6. Do not repeat an MCC.
7. Copy every MCC exactly as it appears in the candidate list.
8. Return the MCCs in descending order of semantic relevance.
9. Return ONLY valid JSON.
10. Do NOT include markdown.
11. Do NOT explain your reasoning outside the JSON.

Return EXACTLY this JSON format:

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

        return prompt
