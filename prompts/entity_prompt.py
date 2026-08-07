class EntityPromptBuilder:

    def build_prompt(
        self,
        article_name: str,
        instance_of: str = ""
    ):

        prompt = f"""
You are an expert at understanding real-world entities.

Article Name:
{article_name}

Instance Of:
{instance_of}

The "Instance Of" field is only supporting context.

Your objective is to identify the entity's PRIMARY commercial identity.

For people:
Return the profession for which they are primarily known.

Ignore:
- Wealth
- Investments
- Businesses owned
- Brand endorsements
- Personal life

For companies:
Return the primary business activity.

For places:
Return the dominant commercial activity.

For movies, books, music, TV shows and games:
Return how consumers typically purchase or access them.

Return ONLY the following key-value format.

entity_name:
entity_type:
summary:
primary_business:
industry:
products_services:
target_customers:
business_model:
parent_company:
country:
keywords:
aliases:
predicted_mcc:
predicted_mcc_industry:
predicted_mcc_reason:

Rules

- Do NOT return JSON.
- Do NOT return markdown.
- One field per line.
- Separate list values using "|".
- Leave unknown fields blank.
"""

        return prompt
