class EntityPromptBuilder:

    def build_prompt(
        self,
        article_name: str,
        instance_of: str = ""
    ):

        return f"""
You are an expert at identifying the primary semantic identity of a real-world entity.

Article:
{article_name}

Instance Of:
{instance_of}

Your task is NOT to predict an MCC.

Your task is to create a concise semantic profile that will later be used to retrieve the most relevant Merchant Category Codes.

Rules

- Use both the Article and Instance Of.
- Focus on the PRIMARY identity only.
- Do not describe history or achievements.
- Do not explain your reasoning.
- Do not output JSON.
- Do not output markdown.
- Every field must appear exactly once.
- Leave unknown fields blank.
- Multiple values must be separated using |

Guidelines

People:
Return their profession and the commercial activity people associate with them.

Examples:
Cristiano Ronaldo → Professional Football Player
Taylor Swift → Singer and Performer
Christopher Nolan → Film Director

Companies:
Return the primary business activity.

Countries:
Return the dominant economic and commercial identity.

Movies / TV / Books / Games / Music:
Return how consumers access or purchase them.

Historical Figures:
Return the role for which they are primarily known.

Political Events / Wars / Lists:
Return the main real-world category.

Keywords:
Use 5–10 high-value semantic keywords.
Avoid generic words.

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
"""
