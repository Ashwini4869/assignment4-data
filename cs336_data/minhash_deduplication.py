import os
import random
import re
import string
import unicodedata
from collections import defaultdict
from itertools import combinations
from pathlib import Path


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text


def get_ngrams(text: str, ngram_length: int) -> set[tuple[str, ...]]:
    words = text.split()
    return {tuple(words[i : i + ngram_length]) for i in range(len(words) - ngram_length + 1)}


def compute_minhash(ngrams: set[tuple[str, ...]], num_hashes: int, hash_params: list[tuple[int, int]]) -> list[int]:
    p = (1 << 61) - 1

    signature = [p] * num_hashes

    for ngram in ngrams:
        x = hash(ngram) % p
        for i, (a, b) in enumerate(hash_params):
            value = (a * x + b) % p
            signature[i] = min(signature[i], value)

    return signature


def get_lsh_candidates(signatures: list[list[int]], num_bands: int) -> set[tuple[int, int]]:
    num_hashes = len(signatures[0])
    rows_per_band = num_hashes // num_bands

    buckets = defaultdict(list)

    for doc_id, signature in enumerate(signatures):
        for band in range(num_bands):
            start = band * rows_per_band
            end = start + rows_per_band

            band_signature = tuple(signature[start:end])

            bucket_key = (band, band_signature)
            buckets[bucket_key].append(doc_id)

    candidates = set()
    for documents in buckets.values():
        if len(documents) > 1:
            for doc1, doc2 in combinations(documents, 2):
                candidates.add((doc1, doc2))

    return candidates


def jaccard_similarity(ngrams_a: set[tuple[str, ...]], ngrams_b: set[tuple[str, ...]]) -> float:
    intersection = ngrams_a & ngrams_b
    union = ngrams_a | ngrams_b

    if not union:
        return 1.0

    return len(intersection) / len(union)


def find(parent: list[int], x: int) -> int:
    if parent[x] != x:
        parent[x] = find(parent, parent[x])

    return parent[x]


def union(
    parent: list[int],
    rank: list[int],
    x: int,
    y: int,
) -> None:

    root_x = find(parent, x)
    root_y = find(parent, y)

    if root_x == root_y:
        return

    if rank[root_x] < rank[root_y]:
        parent[root_x] = root_y

    elif rank[root_x] > rank[root_y]:
        parent[root_y] = root_x

    else:
        parent[root_y] = root_x
        rank[root_x] += 1


def minhash_deduplication(
    input_paths: list[os.PathLike],
    num_hashes: int,
    num_bands: int,
    ngrams_length: int,
    jaccard_threshold: float,
    output_dir: os.PathLike,
):
    RANDOM_SEED = 42
    p = (1 << 61) - 1

    rng = random.Random(42)
    hash_params = [
        (
            rng.randint(1, p - 1),
            rng.randint(0, p - 1),
        )
        for _ in range(num_hashes)
    ]
    selection_rng = random.Random(RANDOM_SEED)

    documents = []
    document_ngrams = []

    for input_path in input_paths:
        with open(input_path, encoding="utf-8") as f:
            content = f.read()

        documents.append((input_path, content))

        normalized = normalize_text(content)

        ngrams = get_ngrams(normalized, ngrams_length)

        document_ngrams.append(ngrams)

    num_documents = len(documents)
    if num_documents == 0:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        for input_path in input_paths:
            (output_path / Path(input_path).name).write_text("", encoding="utf-8")
        return

    signatures = []
    for ngrams in document_ngrams:
        signature = compute_minhash(
            ngrams,
            num_hashes,
            hash_params,
        )
        signatures.append(signature)

    candidates = get_lsh_candidates(
        signatures,
        num_bands,
    )

    parent = list(range(num_documents))
    rank = [0] * num_documents

    for doc1, doc2 in candidates:
        similarity = jaccard_similarity(
            document_ngrams[doc1],
            document_ngrams[doc2],
        )

        if similarity > jaccard_threshold:
            union(parent, rank, doc1, doc2)

    clusters = defaultdict(list)
    for doc_id in range(num_documents):
        root = find(parent, doc_id)
        clusters[root].append(doc_id)

    retained_indices = set()

    for cluster in clusters.values():
        selected = selection_rng.choice(cluster)
        retained_indices.add(selected)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    retained_by_file = defaultdict(list)

    for doc_id in sorted(retained_indices):
        input_path, original_content = documents[doc_id]

        retained_by_file[input_path].append(original_content)

    output_names = set()

    for input_path in input_paths:
        if input_path not in retained_by_file:
            continue

        filename = Path(input_path).name

        if filename in output_names:
            raise ValueError(f"Multiple input files have the same filename: {filename}")

        output_names.add(filename)

        output_file = output_path / filename

        with open(output_file, "w", encoding="utf-8", newline="") as f:
            f.writelines(retained_by_file[input_path])
