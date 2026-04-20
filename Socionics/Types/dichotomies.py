def subsets_with_base(labels):
    base = labels[0]
    rest = labels[1:]
    n = len(rest)

    for mask in range(1 << n):
        subset = [base] + [rest[i] for i in range(n) if mask & (1 << i)]
        complement = [x for x in labels if x not in subset]
        yield subset, complement

labels = ["ILE", "SEI", "ESE", "LII", "EIE", "LSI", "SLE", "IEI", "SEE", "ILI", "LIE", "ESI", "LSE", "EII", "IEE", "SLI"]

with open("partitions.txt", "w") as f:
    for s, c in subsets_with_base(labels):
        s_str = "{" + ", ".join(s) + "}"
        c_str = "{" + ", ".join(c) + "}" if c else "∅"
        f.write(f"{s_str}  |  {c_str}\n")
