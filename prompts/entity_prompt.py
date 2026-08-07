class EntityPromptBuilder:

    def build_prompt(
        self,
        article_name: str,
        instance_of: str = ""
    ):

        prompt = f"""
You are an expert at understanding real-world entities.

Input

Article Name:
{article_name}

Instance Of:
{instance_of}

The "Instance Of" field is only supporting context to identify the entity type.

Your job is to identify the entity's PRIMARY commercial identity.

For people:
Return the profession for which they are primarily known.

Examples:
Actor
Singer
Football Player
Author
Politician
Scientist

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

For movies, books, games and music:
Return how consumers primarily access or purchase them.

Return ONLY the following key-value format.

entity_name:
entity_type:
primary_business:
industry:
products_services:
target_customers:
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
- If unknown leave blank.
"""

        return prompt
