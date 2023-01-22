from exercises.chapter2 import exercise1

import pytest
from time import time
import random

@pytest.fixture(scope = 'module')
def all_numbers():
    return list(range(1, 3000001))

@pytest.mark.parametrize("testid", range(10))
def test_binary_contains(all_numbers, testid):
    numbers = [random.choice(all_numbers) for j in range(1000000)]
    sorted_numbers = sorted(numbers)
    number = random.choice(range(3200000//2, 3200001))
    stime = time()
    res = exercise1.linear_contains(sorted_numbers, number)
    etime = time()
    linear_time = etime - stime
    assert res == (number in sorted_numbers)
    stime = time()
    res = exercise1.binary_contains(sorted_numbers, number)
    etime = time()
    binary_time = etime - stime
    assert res == (number in sorted_numbers)
    assert binary_time < 0.1*linear_time

