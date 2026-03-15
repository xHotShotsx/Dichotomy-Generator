import sys
sys.stdout.reconfigure(encoding="utf-8")
from itertools import combinations

TYPES = [
    "αe",  # 0 (base)
    "αi",  # 1
    "βe",  # 2
    "βi",  # 3
    "γe",  # 4
    "γi",  # 5
    "δe",  # 6
    "δi",  # 7
]

def first_halves_balanced_splits(labels, base_label="αe"):

    n = len(labels)
    if n % 2 != 0:
        raise ValueError("n must be even.")
    if base_label not in labels:
        raise ValueError("base_label must be one of the labels.")

    k = n // 2
    rest = [x for x in labels if x != base_label]

    for combo in combinations(rest, k - 1):
        yield (base_label, *combo)

def write_halves_to_file(path="Socionics/Dyadic Elements/Activators/activator_splits_n8.txt", labels=TYPES, base_label="αe"):
    with open(path, "w", encoding="utf-8") as f:
        for half in first_halves_balanced_splits(labels, base_label=base_label):
            f.write(",".join(half) + "\n")

def write_splits_to_file(path="Socionics/Dyadic Elements/Activators/activator_splits_n8.txt", labels=TYPES, base_label="αe"):

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
    print("Done. Generated 35 halves with αe in the first half.")