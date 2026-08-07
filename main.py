from scripts.classifier import MCCClassifier
import pandas as pd


def main():

    classifier = MCCClassifier()

    print("=" * 60)
    print("Merchant Category Code (MCC) Classifier")
    print("=" * 60)

    ####################################################
    # LOAD INPUT
    ####################################################

    input_file = "data/articles_metadata.xlsx"

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
    # TOP 5 MCC COLUMNS
    ####################################################

    prediction_columns = []

    for i in range(1, 6):

        prediction_columns.extend([

            f"rank{i}_mcc",
            f"rank{i}_industry",
            f"rank{i}_reason"

        ])

    ####################################################
    # STATUS
    ####################################################

    misc_columns = [

        "status",
        "error"

    ]

    ####################################################
    # ADD NEW COLUMNS IF MISSING
    ####################################################

    for column in entity_columns + prediction_columns + misc_columns:

        if column not in df.columns:

            df[column] = ""

    ####################################################
    # PROCESS
    ####################################################

    total = len(df)

    output_file = "articles_metadata_output.xlsx"

    for index, row in df.iterrows():

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

            prediction = result["final_prediction"]

            ####################################################
            # ENTITY
            ####################################################

            for key in entity_columns:

                value = entity.get(key, "")

                if isinstance(value, list):

                    value = "; ".join(value)

                df.at[index, key] = value

            ####################################################
            # TOP 5 MCC
            ####################################################

            predictions = prediction.get(

                "top_5_mcc_predictions",

                []

            )

            for i in range(5):

                if i < len(predictions):

                    item = predictions[i]

                    df.at[index, f"rank{i+1}_mcc"] = item.get(
                        "mcc",
                        ""
                    )

                    df.at[index, f"rank{i+1}_industry"] = item.get(
                        "industry",
                        ""
                    )

                    df.at[index, f"rank{i+1}_reason"] = item.get(
                        "reason",
                        ""
                    )

            ####################################################
            # STATUS
            ####################################################

            df.at[index, "status"] = "Success"

            df.at[index, "error"] = ""

        except Exception as e:

            df.at[index, "status"] = "Failed"

            df.at[index, "error"] = str(e)

        ####################################################
        # SAVE AFTER EVERY ARTICLE
        ####################################################

        df.to_excel(

            output_file,

            index=False

        )

    ####################################################
    # DONE
    ####################################################

    print("\n" + "=" * 60)

    print("Processing Complete")

    print(f"Output saved to: {output_file}")

    print("=" * 60)


if __name__ == "__main__":

    main()
