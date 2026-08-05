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
You are an expert Merchant Category Code (MCC) classifier.

Below is the Business Profile generated from Stage 1.

Business Profile

{entity_json}

-------------------------------------------------------

Below are the MOST SEMANTICALLY SIMILAR MCC profiles.

{mcc_text}

-------------------------------------------------------

Your task is to compare ONLY these MCC candidates.

Select the SINGLE closest MCC.

Do NOT invent an MCC.

Do NOT compare against MCCs outside this list.

Return ONLY valid JSON.

IMPORTANT:

Do NOT generate a confidence score based on your own certainty.

The confidence will be calculated later by the application using semantic agreement.

Return EXACTLY:

{{
    "selected_mcc": "",
    "selected_industry": "",
    "selected_reason": ""
}}
"""

        return prompt
