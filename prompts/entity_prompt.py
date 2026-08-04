class EntityPromptBuilder:

    def build_prompt(self, page_name: str):

        prompt = f"""
You are an expert knowledge assistant.

The input below is the title of a Wikipedia article.

Wikipedia Article Title:
{page_name}

Your task is to identify exactly what this article represents.

Use your existing knowledge.

The article may represent a business, person, place, country, historical event, organization, technology, book, movie, landmark, or any other notable entity. If it is not a business, infer the industries, commercial activities, products, services, and merchant domains most closely associated with it. Think from an industry and commercial perspective—consider what industries or businesses a person searching for this Wikipedia topic would most likely be interested in or interact with.

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
    "aliases": []
}}
"""

        return prompt
