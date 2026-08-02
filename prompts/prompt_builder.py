import json


class PromptBuilder:

    def __init__(self):

        with open("data/mcc_codes.json", "r", encoding="utf-8") as f:
            self.mcc_codes = json.load(f)

    def build_prompt(self, page_name: str):

        mcc_text = mcc_text = """
MCC: 2741
Industry: Miscellaneous Publishing and Printing
Description: Publishing and commercial printing services.

MCC: 4899
Industry: Cable, Satellite and Other Pay Television Services
Description: Cable, satellite and streaming pay television providers.

MCC: 5815
Industry: Digital Goods - Media
Description: Online retailers of digital media such as music, movies and books.

MCC: 5818
Industry: Digital Goods - Multi-Category
Description: Online retailers selling multiple categories of digital goods.

MCC: 5968
Industry: Direct Marketing - Continuity/Subscription Merchant
Description: Subscription and recurring billing merchants.
"""

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
        print(prompt)

        return prompt
