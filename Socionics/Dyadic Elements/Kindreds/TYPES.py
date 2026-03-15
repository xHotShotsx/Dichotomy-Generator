TYPES = [
    "Ne",  # 0 (base)
    "Si",  # 1
    "Fe",  # 2
    "Ti",  # 3
    "Se",  # 4
    "Ni",  # 5
    "Te",  # 6
    "Fi",  # 7
]
IDX = {t:i for i,t in enumerate(TYPES)}
FULL_MASK = (1 << 8) - 1

def line_to_mask(line: str) -> int:
    parts = [p.strip() for p in line.strip().split(",") if p.strip()]
    m = 0
    for p in parts:
        m |= 1 << IDX[p]
    return m

def load_masks(path: str) -> list[int]:
    masks = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            s = raw.strip()
            if s:
                if ": " in s:
                    s = s.split(": ", 1)[1]
                masks.append(line_to_mask(s))
    return masks

def xnor_mask(a: int, b: int) -> int:
    return (~(a ^ b)) & FULL_MASK

def passes_symmetry(masks: list[int], i0: int, compare_js0: list[int], half_size: int) -> bool:
    a = masks[i0]
    target = half_size // 2
    for j0 in compare_js0:
        if (a & masks[j0]).bit_count() != target:
            return False
    return True

def report_unique_xnor(
    path: str,
    compare_lines_1based: list[int],
    out_path: str = "Socionics/Dyadic Elements/Kindreds/xnor_unique_report.txt"
):
    masks = load_masks(path)
    n = len(masks)
    half_size = len(TYPES) // 2

    # map mask -> line number (1-based)
    mask_to_line = {masks[i]: i + 1 for i in range(n)}

    compare_js0 = [j - 1 for j in compare_lines_1based]
    compare_masks = [(j, masks[j-1]) for j in compare_lines_1based]

    # If a line number has already appeared as an XNOR output earlier,
    # suppress displaying it when encountered later as a candidate i.
    suppressed_inputs = set()

    # Also avoid repeating the same output lines in the report
    seen_outputs = set()

    kept_inputs = []
    rows = []  # tuples (i, j, out_line)

    for i in range(n, 0, -1):  # descending 6435 -> 1
        if i in suppressed_inputs:
            continue

        i0 = i - 1
        if not passes_symmetry(masks, i0, compare_js0, half_size):
            continue

        a = masks[i0]
        kept_inputs.append(i)

        for (j, b) in compare_masks:
            out_mask = xnor_mask(a, b)
            out_line = mask_to_line[out_mask]  # should always exist in 6435 list

            # record mapping i xnor j -> out_line
            rows.append((i, j, out_line))

            # suppress later display of that output line if it appears as an input
            suppressed_inputs.add(out_line)

            # optional: if you only want unique output lines shown at all
            seen_outputs.add(out_line)

    # Write a compact report
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"Compare lines: {compare_lines_1based}\n")
        f.write(f"Evaluated in descending order: {n} -> 1\n")
        f.write(f"Kept input lines (after suppression): {len(kept_inputs)}\n")
        f.write(f"Total XNOR mappings written: {len(rows)}\n\n")

        # Group by input i for readability
        current_i = None
        for (i, j, out_line) in rows:
            if i != current_i:
                current_i = i
                f.write(f"INPUT line {i}\n")
            f.write(f"  XNOR with line {j} -> OUTPUT line {out_line}\n")

    return kept_inputs, rows, out_path

if __name__ == "__main__":
    path = "Socionics/Dyadic Elements/Kindreds/kindred_splits_n8.txt"
    compare = [1, 21, 24]  # placeholder, adjust as needed
    kept_inputs, rows, out_file = report_unique_xnor(path, compare, out_path="Socionics/Dyadic Elements/Kindreds/xnor_unique_report.txt")
    print("Wrote:", out_file)
    print("Kept inputs:", len(kept_inputs))
    print("First 16 kept inputs:", kept_inputs[:8])
    print("First 16 mappings:", rows[:8])