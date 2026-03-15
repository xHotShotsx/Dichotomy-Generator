from itertools import combinations

TYPES = [
    "ILE",  # 0 (base)
    "SEI",  # 1
    "ESE",  # 2
    "LII",  # 3
    "EIE",  # 4
    "LSI",  # 5
    "SLE",  # 6
    "IEI",  # 7
    "SEE",  # 8
    "ILI",  # 9
    "LIE",  # 10
    "ESI",  # 11
    "LSE",  # 12
    "EII",  # 13
    "IEE",  # 14
    "SLI",  # 15
]

def first_halves_balanced_splits(labels, base_label="ILE"):
    """
    Yield the 'first half' of every balanced split of `labels`,
    forcing `base_label` into the first half to avoid complement duplicates.

    For 16 labels, yields C(15,7)=6435 halves of size 8.
    """
    n = len(labels)
    if n % 2 != 0:
        raise ValueError("n must be even.")
    if base_label not in labels:
        raise ValueError("base_label must be one of the labels.")

    k = n // 2
    rest = [x for x in labels if x != base_label]

    for combo in combinations(rest, k - 1):
        yield (base_label, *combo)

def write_halves_to_file(path="Socionics/Types/socion_halves_n16.txt", labels=TYPES, base_label="ILE"):
    with open(path, "w", encoding="utf-8") as f:
        for half in first_halves_balanced_splits(labels, base_label=base_label):
            f.write(",".join(half) + "\n")

def write_splits_to_file(path="Socionics/Types/socion_splits_n16.txt", labels=TYPES, base_label="ILE"):
    """
    Writes each split as:
    A: <8 labels> | B: <8 labels>
    where A contains base_label and B is its complement.
    """
    universe = set(labels)
    with open(path, "w", encoding="utf-8") as f:
        for half in first_halves_balanced_splits(labels, base_label=base_label):
            A = set(half)
            B = sorted(universe - A)
            f.write("A:" + ",".join(sorted(A)) + " | B:" + ",".join(B) + "\n")

if __name__ == "__main__":
    write_halves_to_file()
    # If you also want complements:
    # write_splits_to_file()
    print("Done. Generated 6435 halves with ILE in the first half.")