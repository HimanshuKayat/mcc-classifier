import json


class MCCPromptBuilder:

    def __init__(self):

        with open("data/mcc_codes.json", "r", encoding="utf-8") as f:
            self.mcc_codes = json.load(f)

    def build_prompt(self, entity_profile):

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

        entity_json = json.dumps(entity_profile, indent=4)

        prompt = f"""
You are an expert Merchant Category Code (MCC) classifier.

Below is a structured business profile of an entity.

Business Profile:

{entity_json}

Below is a database of valid MCC profiles.

{mcc_text}

Your task is to compare the Business Profile against every MCC profile internally.

Do NOT explain your comparison process.

Do NOT list candidate MCCs.

Do NOT rank MCCs.

Do NOT evaluate each MCC one by one.

Perform the comparison internally and return ONLY the single best matching MCC.

If no MCC is a good match, return the closest available MCC from the provided list.

Return EXACTLY one JSON object and nothing else.

{{    "mcc": "0000",
    "industry": "Industry Name",
    "confidence": 0.95,
    "reason": "One concise sentence explaining why this MCC best matches the entity."
}}
"""

        return prompt
