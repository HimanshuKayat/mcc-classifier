import json


class PromptBuilder:

    def __init__(self):

        with open("data/mcc_codes.json", "r", encoding="utf-8") as f:
            self.mcc_codes = json.load(f)

    def build_prompt(self, page_name: str):

        mcc_text = ""

        for item in self.mcc_codes:

            mcc = item.get("mcc", "")
            industry = item.get("industry", "")
            category = item.get("category", "")
            description = item.get("description", "")

            keywords = ", ".join(item.get("keywords", []))
            aliases = ", ".join(item.get("aliases", []))

            mcc_text += (
                f"MCC: {mcc}\n"
                f"Industry: {industry}\n"
                f"Category: {category}\n"
                f"Description: {description}\n"
                f"Keywords: {keywords}\n"
                f"Aliases: {aliases}\n\n"
            )

        prompt = f"""
You are an expert Merchant Category Code (MCC) classifier.

Your task is to classify the merchant below into EXACTLY ONE MCC from the list provided.

Merchant Name:
{page_name}

Available MCC Profiles:

{mcc_text}

Instructions:

- Identify the merchant using your existing knowledge.
- Determine the merchant's primary business or service.
- Compare that business against the complete MCC profile, including Industry, Category, Description, Keywords and Aliases.
- Base your decision on the merchant's primary business activity, not on keyword or name similarity.
- Choose the SINGLE closest matching MCC from the list above.
- Never invent an MCC.
- Return ONLY one valid JSON object.

Return EXACTLY:

{{
    "mcc": "0000",
    "industry": "Industry Name",
    "confidence": 0.95,
    "reason": "One concise sentence explaining the match."
}}
"""

        return prompt
