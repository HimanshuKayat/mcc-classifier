import json


class PromptBuilder:

    def __init__(self):

        with open("data/mcc_codes.json", "r", encoding="utf-8") as f:
            self.mcc_codes = json.load(f)

    def build_prompt(self, page_name: str):

        mcc_text = ""

        for item in self.mcc_codes:

            description = item.get("description", "")

            mcc_text += (
                f"MCC: {item['mcc']}\n"
                f"Industry: {item['industry']}\n"
                f"Description: {description}\n\n"
            )

        prompt = f"""
You are an expert Merchant Category Code (MCC) classification engine.

Your ONLY task is to determine the SINGLE most appropriate Merchant Category Code (MCC) for the merchant provided.

=========================
MERCHANT
=========================

Merchant Name:
{page_name}

=========================
AVAILABLE MCC CODES
=========================

{mcc_text}

=========================
HOW TO THINK
=========================

Your goal is NOT to perform keyword matching.

DO NOT choose an MCC because a word in the merchant name appears similar to a word in an MCC description.

Instead, determine WHAT THE MERCHANT ACTUALLY DOES.

Follow this reasoning process internally:

Step 1.
Identify the merchant.

Ask yourself:
"What real company, business, website, application or service is this?"

If you recognize the merchant from your knowledge, use that knowledge.

Step 2.
Determine its primary business activity.

Examples:

Netflix
→ Subscription video streaming platform

Spotify
→ Digital music streaming service

Uber
→ Ride-hailing transportation platform

Amazon
→ Online retail marketplace

Domino's
→ Pizza restaurant

Airbnb
→ Accommodation marketplace

Apple Music
→ Digital music streaming

Google Play
→ Digital applications and digital content

Steam
→ Digital game distribution platform

Step 3.
Ignore superficial similarities.

Do NOT perform lexical matching.

Incorrect reasoning:

Netflix contains "net"
Therefore Telecommunications

Correct reasoning:

Netflix is a subscription-based streaming service.
Streaming is digital media.
Choose the MCC describing digital media.

Step 4.
Compare ONLY the BUSINESS ACTIVITY with every MCC description.

Choose the MCC whose description best represents the merchant's PRIMARY business.

Ignore:

- company name similarity
- spelling similarity
- shared words
- abbreviations
- random associations

The decision must be based ONLY on what the merchant actually sells or provides.

Step 5.
If multiple MCCs appear reasonable, choose the MOST SPECIFIC one.

Prefer the MCC describing the merchant's primary revenue-generating activity.

=========================
RULES
=========================

1. NEVER invent an MCC.
2. ONLY choose from the MCC list above.
3. NEVER output multiple MCCs.
4. NEVER explain your reasoning step-by-step.
5. NEVER use keyword matching.
6. NEVER guess based on spelling.
7. Use your world knowledge to identify the merchant whenever possible.
8. Then map that business to the closest MCC.
9. Return EXACTLY one JSON object.
10. Output NOTHING except valid JSON.

=========================
OUTPUT FORMAT
=========================

Return EXACTLY:

{{
    "mcc": "0000",
    "industry": "Industry Name",
    "confidence": 0.95,
    "reason": "One concise sentence explaining why this merchant belongs to the selected MCC."
}}

Do not include markdown.
Do not include extra text.
Do not include multiple JSON objects.
Do not include an array.
"""

        return prompt
