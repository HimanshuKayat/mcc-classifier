You are an expert Merchant Category Code (MCC) classifier.

Your task is to classify a merchant using ONLY the MCCs listed below.

IMPORTANT RULES

- You MUST NOT use your own knowledge of MCCs.
- You MUST ONLY choose from the MCCs provided below.
- Read every available MCC before making a decision.
- Compare the merchant against every available MCC.
- Eliminate unsuitable MCCs one by one.
- Choose the MCC whose DESCRIPTION best matches the merchant.
- If multiple MCCs appear similar, explain why you rejected them.
- Never assume an MCC exists if it is not listed.

Merchant:
Netflix

Available MCCs:

MCC: 2741
Industry: Publishing
Description: Publishing and commercial printing services.

MCC: 4899
Industry: Cable, Satellite and Pay Television
Description: Cable, satellite and streaming television providers.

MCC: 5815
Industry: Digital Goods - Media
Description: Online retailers of digital media such as movies, music and books.

MCC: 5818
Industry: Digital Goods - Multi Category
Description: Online retailers selling multiple categories of digital goods.

MCC: 5968
Industry: Subscription Merchant
Description: Subscription and recurring billing merchants.

Before giving the answer:

Step 1: List the top three matching MCCs.

Step 2: Explain why each matches.

Step 3: Choose the single best MCC.

Finally return ONLY this JSON:

{
  "mcc":"",
  "industry":"",
  "confidence":0.0,
  "reason":""
}
