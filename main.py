from scripts.classifier import MCCClassifier
import pandas as pd
import os


def main():

    classifier = MCCClassifier()

    print("=" * 60)
    print("Merchant Category Code (MCC) Classifier")
    print("=" * 60)

    ####################################################
    # INPUT / OUTPUT
    ####################################################

    input_file = "data/articles_metadata.xlsx"
    output_file = "articles_metadata_output.xlsx"

    if os.path.exists(output_file):
        df = pd.read_excel(output_file)
        print("Resuming from existing output file.")
    else:
        df = pd.read_excel(input_file)

    ####################################################
    # ENTITY COLUMNS
    ####################################################

    entity_columns = [

        "entity_name",
        "entity_type",
        "primary_business",
        "industry",
        "products_services",
        "target_customers",
        "country",
        "keywords",
        "aliases"

    ]

    ####################################################
    # PREDICTION COLUMNS
    ####################################################

    prediction_columns = []

    for i in range(1, 6):

        prediction_columns.extend([

            f"rank{i}_mcc",

            f"rank{i}_industry",

            f"rank{i}_reason",

            f"rank{i}_confidence"

        ])

    ####################################################
    # STATUS
    ####################################################

    misc_columns = [

        "status",

        "error"

    ]

    ####################################################
    # CREATE MISSING COLUMNS
    ####################################################

    for column in entity_columns + prediction_columns + misc_columns:

        if column not in df.columns:

            df[column] = ""

    ####################################################
    # PROCESS
    ####################################################

    total = len(df)

    success = 0
    failed = 0

    for index, row in df.iterrows():

        ####################################################
        # RESUME SUPPORT
        ####################################################

        if str(row["status"]).strip() == "Success":

            continue

        article_name = ""

        if not pd.isna(row["article"]):

            article_name = str(

                row["article"]

            ).strip()

        instance_of = ""

        if not pd.isna(row["instance_of"]):

            instance_of = str(

                row["instance_of"]

            ).strip()

        print(f"[{index + 1}/{total}] {article_name}")

        try:

            result = classifier.classify(

                article_name,

                instance_of

            )

            entity = result["entity_profile"]

            predictions = result["final_prediction"][
                "top_5_mcc_predictions"
            ]

            ####################################################
            # ENTITY
            ####################################################

            for key in entity_columns:

                value = entity.get(key, "")

                if isinstance(value, list):

                    value = "; ".join(value)

                df.at[index, key] = value

            ####################################################
            # PREDICTIONS
            ####################################################

            for i, prediction in enumerate(predictions):

                rank = i + 1

                df.at[index, f"rank{rank}_mcc"] = prediction.get(

                    "mcc",

                    ""

                )

                df.at[index, f"rank{rank}_industry"] = prediction.get(

                    "industry",

                    ""

                )

                df.at[index, f"rank{rank}_reason"] = prediction.get(

                    "reason",

                    ""

                )

                df.at[index, f"rank{rank}_confidence"] = prediction.get(

                    "confidence",

                    ""

                )

            df.at[index, "status"] = "Success"
            df.at[index, "error"] = ""

            success += 1

        except Exception as e:

            failed += 1

            df.at[index, "status"] = "Failed"

            df.at[index, "error"] = str(e)

        ####################################################
        # SAVE EVERY ROW
        ####################################################

        df.to_excel(

            output_file,

            index=False

        )

    ####################################################
    # SUMMARY
    ####################################################

    print("\n" + "=" * 60)

    print("Processing Complete")

    print(f"Total    : {total}")
    print(f"Success  : {success}")
    print(f"Failed   : {failed}")

    print(f"\nOutput saved to: {output_file}")

    print("=" * 60)


if __name__ == "__main__":

    main()
