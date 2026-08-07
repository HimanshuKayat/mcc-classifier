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
                f"Keywords: {', '.join(item.get('keywords', []))}\n"
                f"Aliases: {', '.join(item.get('aliases', []))}\n"
                "------------------------------------------------------------\n"
            )

        prompt = f"""
You are an expert Merchant Category Code (MCC) classifier.

ENTITY PROFILE

{entity_json}

AVAILABLE MCC CANDIDATES

{mcc_text}

TASK

Select the FIVE MCCs that are the strongest semantic matches for the entity.

Base your decision primarily on:

- Primary commercial activity
- Business model
- Products and services
- Customer transaction
- Industry
- Description

Guidelines

- Companies → classify by primary revenue-generating activity.
- Products → classify by where the product is normally purchased.
- Places → classify by dominant commercial activity.
- People → classify by the commercial activity most associated with them (movies, music, sports, books, education, merchandise, travel, etc.).
- Movies, TV shows, books, games and events → classify by how consumers purchase or access them.

Rules

1. Choose ONLY from the MCC candidates provided.
2. Never invent an MCC.
3. Return EXACTLY five different MCCs.
4. Rank from best match to fifth-best match.
5. The first MCC should be the single best overall match.
6. Return ONLY valid JSON.
7. No explanations outside the JSON.

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
