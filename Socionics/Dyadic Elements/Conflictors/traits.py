from itertools import combinations

TYPES = [
    "?(N|F)",  # 0 (base)
    "!(S|T)",  # 1
    "!(N|F)",  # 2
    "?(S|T)",  # 3
    "?(S|F)",  # 4
    "!(N|T)",  # 5
    "!(S|F)",  # 6
    "?(N|T)",  # 7
]

def first_halves_balanced_splits(labels, base_label="?(N|F)"):

    n = len(labels)
    if n % 2 != 0:
        raise ValueError("n must be even.")
    if base_label not in labels:
        raise ValueError("base_label must be one of the labels.")

    k = n // 2
    rest = [x for x in labels if x != base_label]

    for combo in combinations(rest, k - 1):
        yield (base_label, *combo)

def write_halves_to_file(path="Socionics/Dyadic Elements/Conflictors/conflictor_splits_n8.txt", labels=TYPES, base_label="?(N|F)"):
    with open(path, "w", encoding="utf-8") as f:
        for half in first_halves_balanced_splits(labels, base_label=base_label):
            f.write(",".join(half) + "\n")

def write_splits_to_file(path="Socionics/Dyadic Elements/Conflictors/conflictor_splits_n8.txt", labels=TYPES, base_label="?(N|F)"):

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
    print("Done. Generated 35 halves with ?(N|F) in the first half.")