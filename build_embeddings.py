import json
import pickle

from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-large-en-v1.5"


def profile_to_text(profile):

    keywords = " ".join(
        profile.get("keywords", [])
    )

    aliases = " ".join(
        profile.get("aliases", [])
    )

    return f"""
Merchant Category Code: {profile.get("mcc","")}

Industry: {profile.get("industry","")}

Category: {profile.get("category","")}

Merchant Activity: {profile.get("description","")}

Keywords: {keywords}

Aliases: {aliases}
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

    texts = [

        profile_to_text(profile)

        for profile in profiles

    ]

    print(
        f"Generating embeddings for {len(texts)} MCC profiles..."
    )

    embeddings = model.encode(

        texts,

        show_progress_bar=True,

        convert_to_numpy=True,

        normalize_embeddings=True

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
        f"Saved {len(profiles)} embeddings."
    )


if __name__ == "__main__":

    main()
