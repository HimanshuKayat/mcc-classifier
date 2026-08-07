from scripts.classifier import MCCClassifier
import pandas as pd
import json


def main():

    classifier = MCCClassifier()

    print("=" * 60)
    print("Merchant Category Code (MCC) Classifier")
    print("=" * 60)

    ####################################################
    # LOAD INPUT EXCEL
    ####################################################

    input_file = "data/articles_metadata.xlsx"

    df = pd.read_excel(input_file)

    ####################################################
    # ADD OUTPUT COLUMNS
    ####################################################

    if "entity_profile" not in df.columns:
        df["entity_profile"] = ""

    if "mcc_predictions" not in df.columns:
        df["mcc_predictions"] = ""

    if "status" not in df.columns:
        df["status"] = ""

    if "error" not in df.columns:
        df["error"] = ""

    ####################################################
    # PROCESS EACH ROW
    ####################################################

    total = len(df)

    for index, row in df.iterrows():

        article_name = "" if pd.isna(row["article"]) else str(row["article"]).strip()

        instance_of = "" if pd.isna(row["instance_of"]) else str(row["instance_of"]).strip()

        print(
            f"\n[{index + 1}/{total}] Processing: {article_name}"
        )

        try:

            result = classifier.classify(

                article_name,

                instance_of

            )

            entity = result["entity_profile"]

            entity_response = result["entity_response"]

            prediction = result["final_prediction"]

            mcc_response = result["mcc_response"]

            ####################################################
            # STORE ENTITY PROFILE
            ####################################################

            df.at[index, "entity_profile"] = json.dumps(

                entity,

                indent=4,

                ensure_ascii=False

            )

            ####################################################
            # STORE COMPLETE MCC RESULT
            ####################################################

            df.at[index, "mcc_predictions"] = json.dumps(

                prediction,

                indent=4,

                ensure_ascii=False

            )

            ####################################################
            # STATUS
            ####################################################

            df.at[index, "status"] = "Success"

            df.at[index, "error"] = ""

        except Exception as e:

            print(f"Failed: {article_name}")

            print(str(e))

            df.at[index, "status"] = "Failed"

            df.at[index, "error"] = str(e)

    ####################################################
    # SAVE OUTPUT
    ####################################################

    output_file = "articles_metadata_output.xlsx"

    df.to_excel(

        output_file,

        index=False

    )

    print("\n" + "=" * 60)

    print("Processing Complete")

    print(f"Output saved to: {output_file}")

    print("=" * 60)


if __name__ == "__main__":

    main()
