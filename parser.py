import json
import re


class JSONParser:

    LIST_FIELDS = {
        "products_services",
        "target_customers",
        "keywords",
        "aliases"
    }

    @staticmethod
    def parse(response: str):

        if not response:
            raise ValueError("LLM returned an empty response.")

        response = (
            response.replace("```json", "")
                    .replace("```", "")
                    .strip()
        )

        ####################################################
        # TRY TO EXTRACT JSON ANYWHERE IN RESPONSE
        ####################################################

        match = re.search(
            r"\{[\s\S]*\}",
            response
        )

        if match:

            try:
                return json.loads(
                    match.group(0)
                )

            except json.JSONDecodeError:
                pass

        ####################################################
        # FALLBACK TO KEY-VALUE PARSER
        ####################################################

        profile = {}

        for line in response.splitlines():

            line = line.strip()

            if not line or ":" not in line:
                continue

            key, value = line.split(":", 1)

            key = key.strip()

            value = value.strip()

            if key in JSONParser.LIST_FIELDS:

                profile[key] = [

                    item.strip()

                    for item in value.split("|")

                    if item.strip()

                ]

            else:

                profile[key] = value

        if not profile:

            raise ValueError(
                "Unable to parse model response."
            )

        return profile
