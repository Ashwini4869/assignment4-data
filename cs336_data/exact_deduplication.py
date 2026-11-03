import os
from collections import defaultdict


def exact_line_deduplication(input_files: list[os.PathLike], output_directory: os.PathLike):
    counter = defaultdict(int)

    for input_file in input_files:
        with open(input_file) as file:
            for line in file:
                h = hash(line)
                counter[h] += 1

    os.makedirs(output_directory, exist_ok=True)

    for input_file in input_files:
        output_file = os.path.join(output_directory, os.path.basename(input_file))

        with open(input_file) as source, open(output_file, "w") as target:
            for line in source:
                if counter[hash(line)] == 1:
                    target.write(line)
