from typing import Any

import fasttext

NSFW_MODEL_PATH = "data/jigsaw_fasttext_bigrams_nsfw_final.bin"
TOXIC_SPEECH_MODEL_PATH = "data/jigsaw_fasttext_bigrams_hatespeech_final.bin"

nsfw_model = fasttext.load_model(NSFW_MODEL_PATH)
toxic_speech_model = fasttext.load_model(TOXIC_SPEECH_MODEL_PATH)


def classify_nsfw(text: str) -> tuple[Any, float]:
    label, confidence = nsfw_model.predict(text)
    label = label[0].replace("__label__", "")
    confidence = confidence[0]
    return label, confidence


def classify_toxic_speech(text: str) -> tuple[Any, float]:
    label, confidence = toxic_speech_model.predict(text)
    label = label[0].replace("__label__", "")
    confidence = confidence[0]
    return label, confidence
