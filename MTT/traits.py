import sys
sys.stdout.reconfigure(encoding="utf-8")
from itertools import combinations

TYPES = [
    "NTC","SFB","FSB","TNC","NFP","STS","FNP","TSS",
    "FNB","TSC","STC","NFB","FSP","TNS","SFP","NTS",
    "SFC","NTB","TNB","FSC","STP","NFS","TSP","FNS",
    "TSB","FNC","NFC","STB","TNP","FSS","NTP","SFS",
]

def first_halves_balanced_splits(labels, base_label="NTC"):

    n = len(labels)
    if n % 2 != 0:
        raise ValueError("n must be even.")
    if base_label not in labels:
        raise ValueError("base_label must be one of the labels.")

    k = n // 2
    rest = [x for x in labels if x != base_label]

    for combo in combinations(rest, k - 1):
        yield (base_label, *combo)

def write_halves_to_file(path="MTT/type_splits_n32.txt", labels=TYPES, base_label="NTC"):
    with open(path, "w", encoding="utf-8") as f:
        for half in first_halves_balanced_splits(labels, base_label=base_label):
            f.write(",".join(half) + "\n")

def write_splits_to_file(path="MTT/type_splits_n32.txt", labels=TYPES, base_label="NTC"):

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
    print("Done. Generated 30M+ halves with NTC in the first half.")
