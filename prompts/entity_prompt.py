class EntityPromptBuilder:

    def build_prompt(self, page_name: str):

        prompt = f"""
You are an expert knowledge assistant and Merchant Category Code (MCC) expert.

The input below is the title of a Wikipedia article or merchant/entity name.

Input:
{page_name}

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
