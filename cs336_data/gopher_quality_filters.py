def gopher_quality_filter(text: str) -> bool:
    words = text.split()
    word_count = len(words)

    if not (50 <= word_count <= 100_000):
        return False

    mean_length = sum(len(word) for word in words) / len(words) if words else 0
    if not (3 <= mean_length <= 10):
        return False

    lines = text.splitlines()
    if lines:
        ellipsis_fraction = sum(line.rstrip().endswith("...") for line in lines) / len(lines)

        if ellipsis_fraction > 0.30:
            return False

    alphabetic_fraction = sum(any(char.isalpha() for char in word) for word in words) / word_count

    return alphabetic_fraction >= 0.80
