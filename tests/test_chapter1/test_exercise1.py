from exercises.chapter1 import exercise1

import pytest

@pytest.mark.parametrize("n", list(range(0, 50))+list(range(100, 50, -1)))
def test_solution(n):
    result = exercise1.solution(n)
    if n == 0:
        correct = 0
    else:
        correct = exercise1.fib5(n)
    
    assert result == correct
    