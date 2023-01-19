
# listings 1.10 and 1.11
class CompressedGene:
    def __init__(self, gene: str) -> None:
        self._compress(gene)

    def _compress(self, gene: str) -> None:
        self.bit_string: int = 1 # start with sentinel
        for nucleotide in gene.upper():
            self.bit_string <<= 2 # shift left two bits
            if nucleotide == "A": # change last two bits to 00
                self.bit_string |= 0b00
            elif nucleotide == "C": # change last two bits to 01
                self.bit_string |= 0b01
            elif nucleotide == "G": # change last two bits to 10
                self.bit_string |= 0b10
            elif nucleotide == "T": # change last two bits to 11
                self.bit_string |= 0b11
            else:
                raise ValueError("Invalid Nucleotide:{}".format(nucleotide))

    def decompress(self) -> str:
        gene: str = ""
        for i in range(0, self.bit_string.bit_length() - 1, 2): # - 1 to exclude sentinel
            bits: int = self.bit_string >> i & 0b11 # get just 2 relevant bits
            if bits == 0b00: # A
                gene += "A"
            elif bits == 0b01: # C
                gene += "C"
            elif bits == 0b10: # G
                gene += "G"
            elif bits == 0b11: # T
                gene += "T"
            else:
                raise ValueError("Invalid bits:{}".format(bits))
        return gene[::-1] # [::-1] reverses string by slicing backward

    def __str__(self) -> str: # string representation for pretty printing
        return self.decompress()

from typing import Type

class Intbs(object):
    """
    Simple wrapper around int to function as bitstring
    """
    def __init__(self, val=0):
        self.val = 0
    
    def __getitem__(self, idx):
        return (self.val >> idx) & 1

    def __setitem__(self, idx, val):
        currval = self[idx]
        if not (currval == val):
            self.val |= (1 << idx)

    def __iter__(self):
        self.__current = 0
        return self

    def __next__(self):
        if self.val < 1<<(self.__current):
            self.__current = 0
            raise StopIteration
        else:
            res = (self.val >> self.__current) & 1
            self.__current += 1
            return res

class MyCompressedGene:
    def __init__(self, gene: str) -> None:
        self._compress(gene)

    def _compress(self, gene: str) -> None:
        self.bit_string: Type[Intbs] = Intbs()
        for j, nucleotide in enumerate(gene.upper()):
            if nucleotide == "A": # change last two bits to 00
                self.bit_string[2*j], self.bit_string[(2*j) + 1] = 0, 0
            elif nucleotide == "C": # change last two bits to 01
                self.bit_string[2*j], self.bit_string[(2*j) + 1] = 1, 0
            elif nucleotide == "G": # change last two bits to 10
                self.bit_string[2*j], self.bit_string[(2*j) + 1] = 0, 1
            elif nucleotide == "T": # change last two bits to 11
                self.bit_string[2*j], self.bit_string[(2*j) + 1] = 1, 1
            else:
                raise ValueError("Invalid Nucleotide:{}".format(nucleotide))
        self.bit_string[(2*j)+2] = 1 # sentinel

    def decompress(self) -> str:
        gene: str = ""
        for j, bit in enumerate(self.bit_string):
            if j%2 == 0:
                prevbit:int = bit
                continue
            else:
                currbit: int = bit
                bits: int = prevbit + (2*currbit)
            if bits == 0b00: # A
                gene += "A"
            elif bits == 0b01: # C
                gene += "C"
            elif bits == 0b10: # G
                gene += "G"
            elif bits == 0b11: # T
                gene += "T"
            else:
                raise ValueError("Invalid bits:{}".format(bits))
        return gene

    def __str__(self) -> str: # string representation for pretty printing
        return self.decompress()

if __name__ == "__main__":
    from sys import getsizeof
    original: str = "TAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATATAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATA" * 100

    print("===== FROM BOOK =====")

    print("original is {} bytes".format(getsizeof(original)))
    compressed: CompressedGene = CompressedGene(original) # compress
    print("compressed is {} bytes".format(getsizeof(compressed.bit_string)))
    tmp = compressed.bit_string
    print("original and decompressed are the same: {}".format(original == compressed.decompress()))

    print("===== MY VERSION =====")
    print("original is {} bytes".format(getsizeof(original)))
    compressed: MyCompressedGene = MyCompressedGene(original) # compress
    print("compressed is {} bytes".format(getsizeof(compressed.bit_string.val)))
    print("original and decompressed are the same: {}".format(original == compressed.decompress()))


