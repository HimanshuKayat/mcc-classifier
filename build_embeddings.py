import json
import pickle

from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def profile_to_text(profile):

    keywords = " | ".join(
        profile.get("keywords", [])
    )

    aliases = " | ".join(
        profile.get("aliases", [])
    )

    return f"""
Merchant Category Code:
{profile.get("mcc","")}

Industry:
{profile.get("industry","")}

Industry:
{profile.get("industry","")}

Merchant Category:
{profile.get("category","")}

Merchant Activity:
{profile.get("description","")}

Merchant Activity:
{profile.get("description","")}

Keywords:
{keywords}

Keywords:
{keywords}

Aliases:
{aliases}
"""


def main():

    print("Loading embedding model...")

    model = SentenceTransformer(
        MODEL_NAME
    )

    print("Loading MCC profiles...")

    with open(
        "data/mcc_codes.json",
        "r",
        encoding="utf-8"
    ) as f:

        profiles = json.load(f)

    texts = []

    for profile in profiles:

        texts.append(
            profile_to_text(profile)
        )

    print(
        f"Generating embeddings for {len(texts)} MCC profiles..."
    )

    embeddings = model.encode(

        texts,

        show_progress_bar=True,

        convert_to_numpy=True

    )

    with open(
        "data/mcc_embeddings.pkl",
        "wb"
    ) as f:

        pickle.dump(

            {

                "profiles": profiles,

                "embeddings": embeddings

            },

            f

        )

    print()

    print("Done!")

    print(
        f"Saved {len(profiles)} embeddings to data/mcc_embeddings.pkl"
    )


if __name__ == "__main__":

    main()
