from itertools import combinations

TYPES = [
    "Pe(T.)",  # 0 (base)
    "Pi(F.)",  # 1
    "Je(S.)",  # 2
    "Ji(N.)",  # 3
    "Je(N.)",  # 4
    "Ji(S.)",  # 5
    "Pe(F.)",  # 6
    "Pi(T.)",  # 7
]

def first_halves_balanced_splits(labels, base_label="Pe(T.)"):

    n = len(labels)
    if n % 2 != 0:
        raise ValueError("n must be even.")
    if base_label not in labels:
        raise ValueError("base_label must be one of the labels.")

    k = n // 2
    rest = [x for x in labels if x != base_label]

    for combo in combinations(rest, k - 1):
        yield (base_label, *combo)

def write_halves_to_file(path="Socionics/Dyadic Elements/Lookalikes/lookalike_splits_n8.txt", labels=TYPES, base_label="Pe(T.)"):
    with open(path, "w", encoding="utf-8") as f:
        for half in first_halves_balanced_splits(labels, base_label=base_label):
            f.write(",".join(half) + "\n")

def write_splits_to_file(path="Socionics/Dyadic Elements/Lookalikes/lookalike_splits_n8.txt", labels=TYPES, base_label="Pe(T.)"):

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
    print("Done. Generated 35 halves with Pe(T.) in the first half.")