import random
from typing import Any

import fasttext
from extract_documents import extract_documents

LANGUAGE_MODEL_PATH = "data/lid.176.bin"
model = fasttext.load_model(LANGUAGE_MODEL_PATH)


def identify_language(text) -> tuple[Any, float]:
    text = text.replace("\n", " ").replace("\r", " ")

    labels, probabilities = model.predict(text)

    language = labels[0].replace("__label__", "")
    score = probabilities[0]

    return language, score


def identify_language_warc_documents(warc_file):
    documents = extract_documents(warc_file)
    samples = random.sample(documents, min(20, len(documents)))

    for i, doc in enumerate(samples, 1):
        language, confidence = identify_language(doc["text"])
        print(f"Document {i}: Language {language} Confidence {confidence}")


if __name__ == "__main__":
    identify_language_warc_documents("data/CC-MAIN-20260305070756-20260305100756-00000.warc.gz")
