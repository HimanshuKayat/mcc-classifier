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

The input below is a Wikipedia article title.

Wikipedia Article Title:
{page_name}

Below is a database of valid MCC profiles.

{mcc_text}

Your task is to classify the article into EXACTLY ONE MCC.

Instructions:

- First identify what the Wikipedia article represents.
- Determine the primary business or commercial activity associated with the article.
- Compare the article against every MCC profile using all available information, including the Industry, Category, Description, Keywords and Aliases.
- Base your decision on the overall business activity of the entity, not on keyword or name similarity.
- Select the single closest matching MCC profile.
- Never invent an MCC.
- Return ONLY one valid JSON object.

Return EXACTLY:

{{
    "mcc": "0000",
    "industry": "Industry Name",
    "confidence": 0.95,
    "reason": "One concise sentence explaining why the selected MCC is the closest match."
}}
"""

        return prompt
