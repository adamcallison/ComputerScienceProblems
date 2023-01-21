from exercises.chapter1 import exercise3

import pytest
from typing import TypeVar, Generic, List, Tuple
T = TypeVar('T')

class HanoiTestingStack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    def push(self, item: T) -> None:
        self._container.append(item)
        assert self._container == sorted(self._container)

    def pop(self) -> T:
        return self._container.pop()

    def __repr__(self) -> str:
        return repr(self._container)

@pytest.mark.parametrize("num_discs", range(1, 11))
def test_hanoi_nonrecursive(num_discs: int):
    tower_a: HanoiTestingStack[int] = HanoiTestingStack()
    tower_b: HanoiTestngStack[int] = HanoiTestingStack()
    tower_c: HanoiTestingStack[int] = HanoiTestingStack()
    for i in range(1, num_discs + 1):
        tower_a.push(i)

    exercise3.hanoi_nonrecursive(tower_a, tower_c, tower_b, num_discs)

    assert tower_a._container == []
    assert tower_b._container == []
    assert tower_c._container == list(range(1, num_discs+1))



    