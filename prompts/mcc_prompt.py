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

Your objective is to determine the real-world merchant activity, commercial transaction, or business intent represented by the entity, and then select the MCC whose business profile is semantically the closest match.

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
4. Select the SINGLE MCC that best represents the entity's commercial activity.
5. Do NOT choose an MCC because it shares similar words with the entity.
6. If multiple candidates appear similar, choose the one whose overall business model and customer transaction are the closest semantic match.

CRITICAL RULES

1. You MUST choose EXACTLY ONE MCC.
2. You MUST copy the MCC exactly as it appears in the candidate list.
3. The selected_mcc MUST exist in the retrieved candidate list.
4. Never invent an MCC.
5. Never use an MCC outside the retrieved candidates.
6. Verify that the selected_mcc exists before returning your answer.
7. Return ONLY valid JSON.
8. Do NOT include markdown.
9. Do NOT explain your reasoning outside the JSON.

Return EXACTLY this JSON format:

{{
    "selected_mcc": "",
    "selected_industry": "",
    "selected_reason": ""
}}
"""

        return prompt
