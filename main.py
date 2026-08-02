from scripts.classifier import MCCClassifier


def main():

    classifier = MCCClassifier()

    print("=" * 60)
    print("Merchant Category Code (MCC) Classifier")
    print("=" * 60)

    while True:

        page_name = input("\nEnter article/page name (or type 'exit'): ").strip()

        if page_name.lower() == "exit":
            print("\nGoodbye!")
            break

        result = classifier.classify(page_name)

        print("\nPrediction")
        print("-" * 40)
        print(f"MCC        : {result['mcc']}")
        print(f"Industry   : {result['industry']}")
        print(f"Confidence : {result['confidence']}")
        print(f"Reason     : {result['reason']}")


if __name__ == "__main__":
    main()