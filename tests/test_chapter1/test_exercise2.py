from exercises.chapter1 import exercise2

from sys import getsizeof
import pytest
import random

@pytest.mark.parametrize("testid", range(25))
def test_solution(testid):
    genelength = random.randint(5000, 10000)
    original = ''.join([random.choice('ACTG') for j in range(genelength)])

    compressed = exercise2.CompressedGene(original) # compress
    mycompressed = exercise2.MyCompressedGene(original)
    assert getsizeof(compressed.bit_string) == getsizeof(mycompressed.bit_string.val)

    decompressed = str(mycompressed)

    assert decompressed == original
    