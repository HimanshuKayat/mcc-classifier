from scripts.classifier import MCCClassifier


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
            print("\nGoodbye!")
            break

        result = classifier.classify(page_name)

        entity = result["entity_profile"]

        prediction = result["final_prediction"]

        print()
        print("=" * 60)
        print("MODEL'S UNDERSTANDING")
        print("=" * 60)

        print(f"Entity Name        : {entity.get('entity_name','')}")
        print(f"Entity Type        : {entity.get('entity_type','')}")
        print(f"Merchant Type      : {entity.get('merchant_type','')}")
        print(f"Industry           : {entity.get('industry','')}")
        print(f"Primary Business   : {entity.get('primary_business','')}")

        print()
        print("=" * 60)
        print("MODEL'S INDEPENDENT MCC")
        print("=" * 60)

        print(f"MCC                : {entity.get('predicted_mcc','')}")
        print(f"Industry           : {entity.get('predicted_mcc_industry','')}")
        print(f"Reason             : {entity.get('predicted_mcc_reason','')}")

        print()
        print("=" * 60)
        print("FINAL MAPPED MCC")
        print("=" * 60)

        print(f"MCC                : {prediction.get('selected_mcc','')}")
        print(f"Industry           : {prediction.get('selected_industry','')}")
        print(f"Reason             : {prediction.get('selected_reason','')}")
        print(f"Confidence         : {prediction.get('confidence', 0)}%")

        print()
        print("=" * 60)


if __name__ == "__main__":
    main()
