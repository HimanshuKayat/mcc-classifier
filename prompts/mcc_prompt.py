import json


class MCCPromptBuilder:

    def build_prompt(self, entity_profile, candidate_mccs):

        entity_json = json.dumps(
            entity_profile,
            indent=4,
            ensure_ascii=False
        )

        mcc_text = ""

        for item in candidate_mccs:

            mcc_text += (
                f"MCC: {item.get('mcc', '')}\n"
                f"Industry: {item.get('industry', '')}\n"
                f"Category: {item.get('category', '')}\n"
                f"Description: {item.get('description', '')}\n"
                "----------------------------------------\n"
            )

        prompt = f"""
You are an expert Merchant Category Code (MCC) classifier.

Entity Profile:

{entity_json}

Candidate MCCs:

{mcc_text}

Task:

Choose the FIVE MCCs whose merchant activity best matches the entity.

Rules:

- Use semantic meaning.
- Do not use keyword matching alone.
- Only choose from the candidate MCCs.
- Do not repeat an MCC.
- Rank from best to worst.
- Give a short reason for each choice.
- Return ONLY valid JSON.

Return exactly:

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

        return prompt
