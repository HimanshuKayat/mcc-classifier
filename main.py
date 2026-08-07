from scripts.classifier import MCCClassifier
import pandas as pd
import os

####################################################
# SETTINGS
####################################################

DEBUG = True

INPUT_FILE = "data/articles_metadata.xlsx"

OUTPUT_FILE = "articles_metadata_output.xlsx"


def main():

    classifier = MCCClassifier()

    print("=" * 60)
    print("Merchant Category Code (MCC) Classifier")
    print("=" * 60)

    ####################################################
    # LOAD DATA
    ####################################################

    if os.path.exists(OUTPUT_FILE):

        print("Resuming previous run...\n")

        df = pd.read_excel(
            OUTPUT_FILE
        )

    else:

        df = pd.read_excel(
            INPUT_FILE
        )

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
    # CREATE NEW COLUMNS
    ####################################################

    for column in (

        entity_columns +

        prediction_columns +

        misc_columns

    ):

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

        if str(

            row.get(
                "status",
                ""
            )

        ).strip() == "Success":

            continue

        ####################################################
        # INPUT
        ####################################################

        article_name = ""

        if not pd.isna(

            row["article"]

        ):

            article_name = str(

                row["article"]

            ).strip()

        instance_of = ""

        if not pd.isna(

            row["instance_of"]

        ):

            instance_of = str(

                row["instance_of"]

            ).strip()

        progress = (

            (index + 1)

            / total

        ) * 100

        print(

            f"\n"

            f"[{index+1}/{total}] "

            f"({progress:.1f}%) "

            f"{article_name}"

        )

        ####################################################
        # CLASSIFY
        ####################################################

        try:

            result = classifier.classify(

                article_name,

                instance_of

            )

            entity = result["entity_profile"]

            predictions = result[

                "final_prediction"

            ][

                "top_5_mcc_predictions"

            ]

            ####################################################
            # DEBUG
            ####################################################

            if DEBUG:

                print()

                print("-" * 60)

                print("ENTITY PROFILE")

                print("-" * 60)

                for key, value in entity.items():

                    print(

                        f"{key}: {value}"

                    )

                print()

                print("-" * 60)

                print("TOP 5 MCC PREDICTIONS")

                print("-" * 60)

                for prediction in predictions:

                    print(

                        f"Rank {prediction['rank']}"

                    )

                    print(

                        f"MCC : {prediction['mcc']}"

                    )

                    print(

                        f"Industry : {prediction['industry']}"

                    )

                    print(

                        f"Confidence : "

                        f"{prediction.get('confidence','')}"

                    )

                    print(

                        f"Reason : "

                        f"{prediction['reason']}"

                    )

                    print()

            ####################################################
            # ENTITY COLUMNS
            ####################################################

            for key in entity_columns:

                value = entity.get(

                    key,

                    ""

                )

                if isinstance(

                    value,

                    list

                ):

                    value = "; ".join(value)

                df.at[

                    index,

                    key

                ] = value

            ####################################################
            # PREDICTIONS
            ####################################################

            for i, prediction in enumerate(predictions):

                rank = i + 1

                df.at[
                    index,
                    f"rank{rank}_mcc"
                ] = prediction.get(
                    "mcc",
                    ""
                )

                df.at[
                    index,
                    f"rank{rank}_industry"
                ] = prediction.get(
                    "industry",
                    ""
                )

                df.at[
                    index,
                    f"rank{rank}_reason"
                ] = prediction.get(
                    "reason",
                    ""
                )

                df.at[
                    index,
                    f"rank{rank}_confidence"
                ] = prediction.get(
                    "confidence",
                    ""
                )

            ####################################################
            # STATUS
            ####################################################

            df.at[
                index,
                "status"
            ] = "Success"

            df.at[
                index,
                "error"
            ] = ""

            success += 1

            if not DEBUG:

                print("✓ Success")

        ####################################################
        # FAILED
        ####################################################

        except Exception as e:

            failed += 1

            df.at[
                index,
                "status"
            ] = "Failed"

            df.at[
                index,
                "error"
            ] = str(e)

            print()

            print("ERROR")

            print(str(e))

        ####################################################
        # SAVE AFTER EVERY ROW
        ####################################################

        df.to_excel(

            OUTPUT_FILE,

            index=False

        )

    ####################################################
    # SUMMARY
    ####################################################

    print()

    print("=" * 60)

    print("Processing Complete")

    print("=" * 60)

    print(
        f"Total     : {total}"
    )

    print(
        f"Success   : {success}"
    )

    print(
        f"Failed    : {failed}"
    )

    completed = success + failed

    print(
        f"Completed : {completed}/{total}"
    )

    print()

    print(
        f"Output saved to:\n{OUTPUT_FILE}"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()
