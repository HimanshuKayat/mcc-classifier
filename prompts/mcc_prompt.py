import json


class MCCPromptBuilder:

    def build_prompt(self, entity_profile, candidate_mccs):

        entity_json = json.dumps(
            entity_profile,
            indent=2,
            ensure_ascii=False
        )

        candidates = ""

        for item in candidate_mccs:

            candidates += (
                f"MCC: {item['mcc']}\n"
                f"Industry: {item['industry']}\n"
                f"Category: {item['category']}\n"
                f"Description: {item['description']}\n"
                f"Keywords: {', '.join(item.get('keywords', []))}\n"
                "--------------------------------------------------\n"
            )

        return f"""
You are an expert Visa and Mastercard Merchant Category Code (MCC) classifier.

Your task is to identify which merchant category best represents the PRIMARY COMMERCIAL ACTIVITY of the entity.

ENTITY

{entity_json}

AVAILABLE MCC CANDIDATES

{candidates}

Instructions

- Consider ONLY the MCC candidates provided above.
- Never invent an MCC.
- Never repeat an MCC.
- Determine the entity's PRIMARY commercial activity.
- Ignore popularity, fame, historical importance, politics, ownership, wealth and unrelated facts.
- Compare the entity's commercial activity against every candidate.
- Select the five candidates that best represent how a customer would transact with this entity.
- Rank from strongest semantic match to weakest.
- If two MCCs are similar, prefer the more specific one.
- Return ONLY valid JSON.
- Do not explain your reasoning outside the JSON.

Output Format

{{
  "top_5_mcc_predictions": [
    {{
      "rank": 1,
      "mcc": "",
      "industry": "",
      "reason": ""
    }},
    {{
      "rank": 2,
      "mcc": "",
      "industry": "",
      "reason": ""
    }},
    {{
      "rank": 3,
      "mcc": "",
      "industry": "",
      "reason": ""
    }},
    {{
      "rank": 4,
      "mcc": "",
      "industry": "",
      "reason": ""
    }},
    {{
      "rank": 5,
      "mcc": "",
      "industry": "",
      "reason": ""
    }}
  ]
}}
"""
