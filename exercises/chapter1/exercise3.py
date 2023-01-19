# listing 1.20
from typing import TypeVar, Generic, List, Tuple
T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    def __repr__(self) -> str:
        return repr(self._container)

# listing 1.22
def hanoi(begin: Stack[int], end: Stack[int], temp: Stack[int], n: int) -> None:
    if n == 1:
        end.push(begin.pop())
    else:
        hanoi(begin, temp, end, n - 1)
        hanoi(begin, end, temp, 1)
        hanoi(temp, end, begin, n - 1)

def myhanoi(begin: Stack[int], end: Stack[int], temp: Stack[int], n: int) -> None:
    recursion_stack: Stack[Tuple[Stack[int], Stack[int], Stack[int], int]]
    recursion_stack.push((begin, end, temp, n))
    while len(recursion_stack._container) > 0:
        # unfinished




if __name__ == '__main__':
    # listing 1.21
    num_discs: int = 3
    tower_a: Stack[int] = Stack()
    tower_b: Stack[int] = Stack()
    tower_c: Stack[int] = Stack()
    for i in range(1, num_discs + 1):
        tower_a.push(i)

    # listing 1.23
    hanoi(tower_a, tower_c, tower_b, num_discs)
    print(tower_a)
    print(tower_b)
    print(tower_c)