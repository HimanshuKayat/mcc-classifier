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

Select the SINGLE best matching MCC.

CRITICAL RULES

1. You MUST choose EXACTLY ONE MCC.

2. You MUST copy the MCC exactly as it appears in the candidate list.

3. The selected_mcc MUST exist in the candidate list above.

4. Never invent an MCC.

5. Never use an MCC from your own knowledge.

6. Ignore any MCC not present in the retrieved candidates.

7. Use the business profile to compare against every candidate.

8. Choose the candidate whose Industry, Description, Keywords and Category best match the business profile.

9. Before returning your answer, verify that selected_mcc exists in the candidate list.

10. Return ONLY valid JSON.

11. Do NOT include markdown.

12. Do NOT explain your thinking outside JSON.

Return EXACTLY this JSON format:

{{
    "selected_mcc": "",
    "selected_industry": "",
    "selected_reason": ""
}}
"""

        return prompt
