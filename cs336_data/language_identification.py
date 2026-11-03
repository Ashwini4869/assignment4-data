from typing import Any

import fasttext


def identify_language(text) -> tuple[Any, float]:
    model = fasttext.load_model("data/lid.176.bin")
    text = text.replace("\n", " ").replace("\r", " ")

    labels, probabilities = model.predict(text)

    language = labels[0].replace("__label__", "")
    score = probabilities[0]

    return language, score
