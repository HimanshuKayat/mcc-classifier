import json
import re


class JSONParser:

    @staticmethod
    def parse(response: str):

        if not response:
            raise ValueError("LLM returned an empty response.")

        response = response.strip()

        ####################################################
        # JSON RESPONSE
        ####################################################

        if response.startswith("{"):

            response = response.replace(
                "```json",
                ""
            ).replace(
                "```",
                ""
            ).strip()

            match = re.search(
                r"\{.*\}",
                response,
                re.DOTALL
            )

            if not match:
                raise ValueError(
                    "No JSON object found."
                )

            return json.loads(
                match.group()
            )

        ####################################################
        # KEY-VALUE RESPONSE
        ####################################################

        profile = {}

        list_fields = {

            "products_services",

            "target_customers",

            "keywords",

            "aliases"

        }

        for line in response.splitlines():

            line = line.strip()

            if not line:
                continue

            if ":" not in line:
                continue

            key, value = line.split(":", 1)

            key = key.strip()

            value = value.strip()

            if key in list_fields:

                profile[key] = [

                    item.strip()

                    for item in value.split("|")

                    if item.strip()

                ] if value else []

            else:

                profile[key] = value

        return profile
