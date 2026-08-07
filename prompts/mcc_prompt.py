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
You are an expert Visa/Mastercard Merchant Category Code classifier.

ENTITY

{entity_json}

AVAILABLE MCC CANDIDATES

{candidates}

Instructions

- Choose ONLY from the MCC candidates above.
- Never invent an MCC.
- Never repeat an MCC.
- Rank the FIVE best semantic matches.
- Match the commercial activity, not keywords.
- Ignore word overlap.
- Return ONLY valid JSON.

Output format

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
