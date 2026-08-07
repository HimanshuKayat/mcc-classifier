class EntityPromptBuilder:

    def build_prompt(
        self,
        article_name: str,
        instance_of: str = ""
    ):

        prompt = f"""
You are an expert at identifying real-world entities.

Article:
{article_name}

Instance Of:
{instance_of}

Identify the entity's PRIMARY real-world commercial identity.

Rules:

- Use the article title and Instance Of together.
- Instance Of is only supporting context.
- Do NOT explain.
- Do NOT write sentences.
- Do NOT use markdown.
- Do NOT output JSON.
- Output ONLY the fields below.
- Every field must appear exactly once.
- Leave unknown fields blank.
- Separate multiple values using |

For PEOPLE:
Return their profession, not their investments or businesses.

Examples:
Cristiano Ronaldo -> Football Player
Taylor Swift -> Singer
Tim Cook -> Business Executive
Christopher Nolan -> Film Director

For PLACES:
Return the dominant commercial activity.

For COMPANIES:
Return the primary business.

For MOVIES / BOOKS / MUSIC / GAMES:
Return how consumers purchase or access them.

Output exactly:

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
"""

        return prompt
