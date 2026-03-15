from __future__ import annotations

from itertools import permutations, product
from typing import List, Tuple, Dict


LABELS = [
    "αe",  # 0 (base)
    "αi",  # 1
    "βe",  # 2
    "βi",  # 3
    "γe",  # 4
    "γi",  # 5
    "δe",  # 6
    "δi",  # 7
]


# ---------- basic GF(2)^3 utilities ----------

def bit_parity(x: int) -> int:
    return x.bit_count() & 1


def gf2_points(n: int) -> List[int]:
    return list(range(1 << n))


def point_bits(x: int, n: int = 3) -> str:
    return format(x, f"0{n}b")


def apply_linear(cols: Tuple[int, int, int], x: int) -> int:
    """
    Apply a 3x3 GF(2)-matrix whose columns are given as 3-bit integers.
    """
    out = 0
    for i in range(3):
        if (x >> i) & 1:
            out ^= cols[i]
    return out


def is_invertible_matrix(cols: Tuple[int, int, int]) -> bool:
    c1, c2, c3 = cols
    return (
        c1 != 0
        and c2 != 0
        and c3 != 0
        and c1 != c2
        and c1 != c3
        and c2 != c3
        and (c1 ^ c2) != c3
    )


def all_affine_maps_n3() -> List[Tuple[int, ...]]:
    """
    All affine maps x -> A x + b on GF(2)^3, represented as permutations of 0..7.
    Total should be |AGL(3,2)| = 8 * 168 = 1344.
    """
    points = list(range(8))
    nonzero = list(range(1, 8))

    linear_maps = set()
    for cols in product(nonzero, repeat=3):
        if is_invertible_matrix(cols):
            perm = tuple(apply_linear(cols, x) for x in points)
            linear_maps.add(perm)

    affine_maps = set()
    for lin in linear_maps:
        for b in points:
            perm = tuple(lin[x] ^ b for x in points)
            affine_maps.add(perm)

    affine_maps = sorted(affine_maps)
    if len(affine_maps) != 1344:
        raise RuntimeError(f"Expected 1344 affine maps, got {len(affine_maps)}")
    return affine_maps


# ---------- canonical representatives of S8 / AGL(3,2) ----------

def canonical_assignment_under_agl(
    assignment: Tuple[int, ...],
    affine_maps: List[Tuple[int, ...]],
) -> Tuple[int, ...]:
    """
    assignment[p] = label index placed at point p.
    Canonicalize modulo postcomposition by affine maps on the point set.
    """
    reps = []
    for g in affine_maps:
        # new assignment at point p uses old point g[p]
        transformed = tuple(assignment[g[p]] for p in range(8))
        reps.append(transformed)
    return min(reps)


def generate_30_affine_structures(labels: List[str]) -> List[Tuple[int, ...]]:
    """
    Return one canonical representative from each S8 / AGL(3,2) coset.
    Each representative is an assignment:
        point -> label-index
    There should be exactly 30.
    """
    if len(labels) != 8:
        raise ValueError("Need exactly 8 labels for Z2^3 structures.")

    affine_maps = all_affine_maps_n3()
    seen = set()

    for perm in permutations(range(8)):
        canon = canonical_assignment_under_agl(perm, affine_maps)
        seen.add(canon)

    systems = sorted(seen)
    if len(systems) != 30:
        raise RuntimeError(f"Expected 30 systems, got {len(systems)}")
    return systems


# ---------- derive the 7 dichotomies from a chosen affine structure ----------

def standard_linear_hyperplanes() -> List[Tuple[int, ...]]:
    """
    The 7 linear 0-hyperplanes in GF(2)^3, as halves of size 4.
    """
    points = gf2_points(3)
    halves = []
    for functional in range(1, 8):
        half = tuple(sorted(x for x in points if bit_parity(functional & x) == 0))
        halves.append(half)
    return sorted(halves)


def dichotomies_from_assignment(assignment: Tuple[int, ...]) -> List[Tuple[Tuple[int, ...], Tuple[int, ...]]]:
    """
    Convert an affine structure assignment into 7 dichotomies on label indices.
    assignment[p] = label index at point p.
    """
    full = set(range(8))
    result = []

    for half_pts in standard_linear_hyperplanes():
        left = tuple(sorted(assignment[p] for p in half_pts))
        right = tuple(sorted(full - set(left)))
        result.append((left, right))

    return result


# ---------- rendering ----------

def render_assignment(assignment: Tuple[int, ...], labels: List[str]) -> List[str]:
    lines = []
    for point in range(8):
        label = labels[assignment[point]]
        lines.append(f"{point_bits(point)} -> {label}")
    return lines


def render_dichotomies(assignment: Tuple[int, ...], labels: List[str]) -> List[str]:
    lines = []
    dics = dichotomies_from_assignment(assignment)
    for i, (left, right) in enumerate(dics, start=1):
        left_labels = [labels[j] for j in left]
        right_labels = [labels[j] for j in right]
        lines.append(f"d{i}: {','.join(left_labels)} | {','.join(right_labels)}")
    return lines


def write_30_affine_structures(
    out_path: str = "Socionics/Dyadic Elements/Activators/all_30_affine_Z2_3_structures.txt",
    labels: List[str] = LABELS,
) -> None:
    systems = generate_30_affine_structures(labels)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"Labels: {labels}\n")
        f.write(f"Total affine Z2^3 structures: {len(systems)}\n\n")

        for i, assignment in enumerate(systems, start=1):
            f.write(f"System {i}\n")
            f.write("Coordinate assignment:\n")
            for line in render_assignment(assignment, labels):
                f.write(f"  {line}\n")

            f.write("Dichotomies:\n")
            for line in render_dichotomies(assignment, labels):
                f.write(f"  {line}\n")

            f.write("\n")

    print(f"Wrote {len(systems)} systems to {out_path}")


if __name__ == "__main__":
    write_30_affine_structures()
