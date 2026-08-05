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

This prediction must be completely independent and must NOT
assume any external MCC list has been provided.

---------------------------------------------------------

Return ONLY valid JSON.

{{
    "entity_name": "",
    "entity_type": "",
    "summary": "",
    "primary_business": "",
    "industry": "",
    "products_services": [],
    "target_customers": [],
    "business_model": "",
    "parent_company": "",
    "country": "",
    "keywords": [],
    "aliases": [],

    "predicted_mcc": "",
    "predicted_mcc_industry": "",
    "predicted_mcc_reason": ""
}}
"""

        return prompt
