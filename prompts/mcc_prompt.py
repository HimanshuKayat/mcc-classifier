import json


class MCCPromptBuilder:

    def build_prompt(self, entity_profile, candidate_mccs):

        entity_json = json.dumps(entity_profile, indent=4)

        mcc_text = ""

        for item in candidate_mccs:

            mcc_text += (
                f"MCC: {item.get('mcc','')}\n"
                f"Industry: {item.get('industry','')}\n"
                f"Category: {item.get('category','')}\n"
                f"Description: {item.get('description','')}\n"
                f"Keywords: {', '.join(item.get('keywords', []))}\n"
                f"Aliases: {', '.join(item.get('aliases', []))}\n\n"
            )

        prompt = f"""
Your task is to select EXACTLY ONE MCC from the candidate list above.

CRITICAL RULES:

1. You MUST choose one and only one MCC from the candidate list above.

2. The selected_mcc MUST exactly match one of the MCC numbers listed above.

3. If you output an MCC that is NOT present in the candidate list, your answer is INVALID.

4. Do NOT use your own knowledge to invent or recall MCC codes.

5. Ignore any MCC codes you know unless they appear in the candidate list.

6. Before answering, verify that your selected_mcc exists in the candidate list.

Return ONLY valid JSON.

Return EXACTLY:

{{
    "selected_mcc": "",
    "selected_industry": "",
    "selected_reason": ""
}}
"""

        return prompt
