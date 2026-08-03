import json


class PromptBuilder:

    def __init__(self):

        with open("data/mcc_codes.json", "r", encoding="utf-8") as f:
            self.mcc_codes = json.load(f)

    def build_prompt(self, page_name: str):

        mcc_text = ""

        for item in self.mcc_codes:

            description = item.get("description", "")

            mcc_text += (
                f"MCC: {item['mcc']}\n"
                f"Industry: {item['industry']}\n"
                f"Description: {description}\n\n"
            )

        prompt = f"""
You are an expert Merchant Category Code (MCC) classifier.

Your task is to classify the given merchant into exactly ONE Merchant Category Code (MCC).

Merchant Name:
{page_name}

Available MCC Codes:

{mcc_text}

Instructions:

1. Read the merchant name carefully.
2. Compare it against every MCC provided.
3. Use the MCC descriptions while deciding.
4. Choose ONLY ONE MCC.
5. Never invent a new MCC.
6. Return ONLY valid JSON.
7. Do NOT use markdown.
8. Do NOT write explanations outside the JSON.

Return EXACTLY:

{{
    "mcc": "0000",
    "industry": "Industry Name",
    "confidence": 0.95,
    "reason": "One sentence explaining the decision."
}}
"""

        return prompt
