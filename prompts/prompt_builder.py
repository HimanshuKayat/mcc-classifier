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

Your task is to classify the given merchant into exactly ONE MCC from the provided list.

Merchant Name:
{page_name}

Available MCC Entries:

{mcc_text}

Each MCC entry contains:
- MCC Code
- Industry
- Category
- Description
- Keywords
- Aliases

Instructions:

- First identify the merchant using your existing knowledge.
- Determine the merchant's primary business activity.
- Compare that business activity against the complete MCC entry, including the industry, category, description, keywords and aliases.
- Use the entire MCC entry as context, not just the MCC code or description.
- Do not rely on lexical or keyword similarity between the merchant name and an MCC entry.
- Select the SINGLE MCC whose overall business profile best matches the merchant.
- Never invent an MCC.
- Return ONLY one valid JSON object.

Output format:

{
    "mcc": "...",
    "industry": "...",
    "confidence": 0.95,
    "reason": "..."
}
"""

        return prompt
