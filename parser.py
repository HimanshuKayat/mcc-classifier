class JSONParser:

    @staticmethod
    def parse(response: str):

        if not response:
            raise ValueError("LLM returned an empty response.")

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

                if value:

                    profile[key] = [
                        item.strip()
                        for item in value.split("|")
                        if item.strip()
                    ]

                else:

                    profile[key] = []

            else:

                profile[key] = value

        return profile
