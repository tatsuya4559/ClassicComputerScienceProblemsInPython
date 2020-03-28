from enum import IntEnum
from typing import Tuple, List
import bisect


Nucleotide: IntEnum = IntEnum("Nucleotide", ("A", "C", "G", "T"))
Codon = Tuple[Nucleotide, Nucleotide, Nucleotide]
Gene = List[Codon]


def str2gene(s: str) -> Gene:
    gene: Gene = []
    for i in range(0, len(s), 3):
        if (i + 2) >= len(s):
            return gene
        codon: Codon = (Nucleotide[s[i]], Nucleotide[s[i + 1]], Nucleotide[s[i + 2]])
        gene.append(codon)
    return gene


def bisect_contains(gene: Gene, key_codon: Codon) -> bool:
    i = bisect.bisect_left(gene, key_codon)
    if i != len(gene) and gene[i] == key_codon:
        return True
    return False


def main() -> None:
    gene_str: str = "AGCAATACGGGTAAGCTAGTGTTGAAAATCGTTGACCCCATGATGGTGGG"
    my_gene: Gene = str2gene(gene_str)

    acg: Codon = (Nucleotide.A, Nucleotide.C, Nucleotide.G)
    gat: Codon = (Nucleotide.G, Nucleotide.A, Nucleotide.T)
    print(acg in my_gene)
    print(gat in my_gene)
    print(bisect_contains(sorted(my_gene), acg))
    print(bisect_contains(sorted(my_gene), gat))


if __name__ == "__main__":
    main()
