from scripts.classifier import MCCClassifier


def main():

    classifier = MCCClassifier()

    print("=" * 60)
    print("Merchant Category Code (MCC) Classifier")
    print("=" * 60)

    while True:

        page_name = input("\nEnter page name (or exit): ").strip()

        if page_name.lower() == "exit":
            break

        result = classifier.classify(page_name)

        print("\nPrediction")
        print("-" * 40)
        print("MCC:", result["mcc"])
        print("Industry:", result["industry"])
        print("Confidence:", result["confidence"])
        print("Reason:", result["reason"])


if __name__ == "__main__":
    main()
