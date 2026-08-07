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

Select ONLY from the candidate MCCs above.

Interpret the entity as follows:

• Person → classify according to their profession or the commercial activity consumers associate with them.
  Examples:
  Actor → Motion Pictures
  Singer → Music
  Football Player → Sports
  Author → Books

• Company → primary business activity.

• Place → dominant commercial activity.

• Country/City → tourism, transport, government or other dominant commercial activity.

• Movie / TV Show → how consumers purchase or watch it.

• Book → bookstore or publishing.

• Software / App → software or digital services.

Rules

- Choose ONLY from the candidate list.
- Never invent an MCC.
- Never repeat an MCC.
- Rank the FIVE strongest semantic matches.
- Base the decision on commercial activity, not keyword overlap.
- Return ONLY valid JSON.

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
