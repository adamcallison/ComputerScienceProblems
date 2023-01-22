# from listing 2.9
from __future__ import annotations
from typing import TypeVar, Iterable, Sequence, Generic, List, Callable, Set, Deque, Dict, Any, Optional
from typing_extensions import Protocol
from heapq import heappush, heappop
T = TypeVar('T')

# ==== BEGIN MY SOLUTION ===
# exercise is to use the generic functions on a list of 1,000,000 elements, will do at end of file
# ==== END MY SOLUTION ===

# listing 2.1
from enum import IntEnum
from typing import Tuple, List
Nucleotide: IntEnum = IntEnum('Nucleotide', ('A', 'C', 'G', 'T'))

# listing 2.2
Codon = Tuple[Nucleotide, Nucleotide, Nucleotide] # type alias for codons
Gene = List[Codon] # type alias for genes

# listing 2.4
def string_to_gene(s: str) -> Gene:
    gene: Gene = []
    for i in range(0, len(s), 3):
        if (i + 2) >= len(s): # don't run off end!
            return gene
        # initialize codon out of three nucleotides
        codon: Codon = (Nucleotide[s[i]], Nucleotide[s[i + 1]], Nucleotide[s[i + 2]])
        gene.append(codon) # add codon to gene
    return gene

# listing 2.6 (part1)
def linear_contains_codon(gene: Gene, key_codon: Codon) -> bool:
    for codon in gene:
        if codon == key_codon:
            return True
    return False

# listing 2.7
def binary_contains_codon(gene: Gene, key_codon: Codon) -> bool:
    low: int = 0
    high: int = len(gene) - 1
    while low <= high: # while there is still a search space
        mid: int = (low + high) // 2
        if gene[mid] < key_codon:
            low = mid + 1
        elif gene[mid] > key_codon:
            high = mid - 1
        else:
            return True
    return False

# listing 2.9 (most)
def linear_contains(iterable: Iterable[T], key: T) -> bool:
    for item in iterable:
        if item == key:
            return True
    return False

C = TypeVar("C", bound="Comparable")

class Comparable(Protocol):
    def __eq__(self, other: Any) -> bool:
        ...

    def __lt__(self: C, other: C) -> bool:
        ...

    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and self != other

    def __le__(self: C, other: C) -> bool:
        return self < other or self == other

    def __ge__(self: C, other: C) -> bool:
        return not self < other

def binary_contains(sequence: Sequence[C], key: C) -> bool:
    low: int = 0
    high: int = len(sequence) - 1
    while low <= high: # while there is still a search space
        mid: int = (low + high) // 2
        if sequence[mid] < key:
            low = mid + 1
        elif sequence[mid] > key:
            high = mid - 1
        else:
            return True
    return False

if __name__ == '__main__':

    # listing 2.3
    gene_str: str = "ACGTGGCTCTCTAACGTACGTACGTACGGGGTTTATATATACCCTAGGACTCCCTTT"

    # listing 2.5
    my_gene: Gene = string_to_gene(gene_str)

    # listing 2.6 (part2)
    acg: Codon = (Nucleotide.A, Nucleotide.C, Nucleotide.G)
    gat: Codon = (Nucleotide.G, Nucleotide.A, Nucleotide.T)

    print(f"Linear search for {acg} in {gene_str}..." )
    print(linear_contains_codon(my_gene, acg)) # True
    print(f"Linear search for {gat} in {gene_str}..." )
    print(linear_contains_codon(my_gene, gat)) # False

    # listing 2.8
    my_sorted_gene: Gene = sorted(my_gene)
    print(f"Binary search for {acg} in {gene_str}..." )
    print(binary_contains_codon(my_sorted_gene, acg)) # True
    print(f"Binary search for {gat} in {gene_str}..." )
    print(binary_contains_codon(my_sorted_gene, gat)) # False

    # listing 2.9 (rest)
    print(f"Assorted searches using generic functions...")
    print(linear_contains([1, 5, 15, 15, 15, 15, 20], 5)) # True
    print(binary_contains(["a", "d", "e", "f", "z"], "f")) # True
    print(binary_contains(["john", "mark", "ronald", "sarah"], "sheila")) # False

    print("==============================")
    print("~~~Exercise1 solution~~~")
    from time import time
    import random
    print("Generating list of 1,000,000 numbers from 1 to 3,000,000...")
    all_numbers = list(range(1, 3000001))
    numbers = [random.choice(all_numbers) for j in range(1000000)]
    print("Sorting list...")
    sorted_numbers = sorted(numbers)
    print("Choosing a number from 1 to 3,200,000")
    number = random.choice(range(1, 3200001))
    stime = time()
    res = linear_contains(sorted_numbers, number)
    etime = time()
    print(f"Number {number}{' not ' if not res else ' '}found. Linear search took {etime-stime}s.")
    stime = time()
    res = binary_contains(sorted_numbers, number)
    etime = time()
    print(f"Number {number}{' not ' if not res else ' '}found. Binary search took {etime-stime}s.")

