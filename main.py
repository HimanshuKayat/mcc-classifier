from scripts.classifier import MCCClassifier
import json


def main():

    classifier = MCCClassifier()

    print("=" * 60)
    print("Merchant Category Code (MCC) Classifier")
    print("=" * 60)

    while True:

        page_name = input(
            "\nEnter article/page name (or type 'exit'): "
        ).strip()

        if page_name.lower() == "exit":
            break

        result = classifier.classify(page_name)

        entity = result["entity_profile"]
        prediction = result["final_prediction"]

        output = {
            "entity_name": entity.get("entity_name", ""),
            "entity_type": entity.get("entity_type", ""),
            "summary": entity.get("summary", ""),
            "primary_business": entity.get("primary_business", ""),
            "industry": entity.get("industry", ""),
            "products_services": entity.get("products_services", []),
            "target_customers": entity.get("target_customers", []),
            "business_model": entity.get("business_model", ""),
            "parent_company": entity.get("parent_company", ""),
            "country": entity.get("country", ""),
            "keywords": entity.get("keywords", []),
            "aliases": entity.get("aliases", []),
            "top_5_mcc_predictions": prediction.get(
                "top_5_mcc_predictions",
                []
            )
        }

        print()
        print(json.dumps(
            output,
            indent=4,
            ensure_ascii=False
        ))
        print()


if __name__ == "__main__":
    main()
