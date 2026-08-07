import json
import pickle

from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-large-en-v1.5"


def profile_to_text(profile):

    parts = []

    ####################################################
    # HIGHEST PRIORITY
    ####################################################

    if profile.get("industry"):
        parts.append(profile["industry"])

    if profile.get("category"):
        parts.append(profile["category"])

    if profile.get("description"):
        parts.append(profile["description"])

    ####################################################
    # KEYWORDS
    ####################################################

    keywords = profile.get(
        "keywords",
        []
    )

    if keywords:

        parts.append(
            ", ".join(keywords)
        )

    ####################################################
    # ALIASES
    ####################################################

    aliases = profile.get(
        "aliases",
        []
    )

    if aliases:

        parts.append(
            ", ".join(aliases)
        )

    ####################################################
    # MCC NUMBER (Lowest Importance)
    ####################################################

    parts.append(
        f"MCC {profile['mcc']}"
    )

    return " | ".join(parts)


def main():

    print("Loading embedding model...")

    model = SentenceTransformer(
        MODEL_NAME
    )

    print("Loading MCC profiles...")

    with open(
        "data/mcc_codes.json",
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

        convert_to_numpy=True,

        normalize_embeddings=True,

        show_progress_bar=True

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

    print("Done.")

    print(
        f"Saved {len(profiles)} embeddings."
    )


if __name__ == "__main__":

    main()
