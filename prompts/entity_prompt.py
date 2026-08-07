class EntityPromptBuilder:

    def build_prompt(
        self,
        article_name: str,
        instance_of: str = ""
    ):

        prompt = f"""
You are an expert knowledge assistant and Merchant Category Code (MCC) expert.

The input below comes from Wikipedia and Wikidata.

Article Name:
{article_name}

Instance Of:
{instance_of}

Definition of "Instance Of":
The "instance_of" field from Wikidata describes what type or class of entity this article represents (for example: company, person, city, country, film, university, museum, sports team, software, etc.).

Use the "instance_of" value only as supporting context to better understand the entity. It should help disambiguate the entity but should NOT override the entity's primary commercial activity when making MCC predictions.

---------------------------------------------------------

STAGE 1 — Entity Understanding

Identify:

- entity_name
- entity_type
- summary
- primary_business
- industry
- products_services
- target_customers
- business_model
- parent_company
- country
- keywords
- aliases

---------------------------------------------------------

STAGE 2 — Independent MCC Prediction

WITHOUT seeing any MCC list,

predict the SINGLE Visa/Mastercard Merchant Category Code
that you believe best represents this entity using ONLY your
existing knowledge.

Also provide:

- predicted_mcc
- predicted_mcc_industry
- predicted_mcc_reason

---------------------------------------------------------

IMPORTANT OUTPUT FORMAT

Return ONLY the following key-value format.

Do NOT return JSON.

Do NOT use markdown.

Do NOT use bullet points.

Each field must appear on exactly one line.

For list fields, separate values using the "|" character.

If a field is unknown, leave it blank.

Output exactly in this format:

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

Example:

entity_name: Netflix
entity_type: Entertainment Company
summary: American streaming media company.
primary_business: Streaming media
industry: Media and Entertainment
products_services: Streaming Services | Original Content
target_customers: Individuals | Households
business_model: Subscription-based
parent_company:
country: United States
keywords: Netflix | Streaming | Entertainment | Movies
aliases:
predicted_mcc: 5961
predicted_mcc_industry: Telecommunications Services
predicted_mcc_reason: Streaming media subscription service.

Return ONLY the key-value pairs.
"""

        return prompt
