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

# ==== BEGIN MY SOLUTION ====
def hanoi_nonrecursive(begin: Stack[int], end: Stack[int], temp: Stack[int], n: int) -> None:
    """
    3-tower hanoi solver with explicit stack to avoid recursion
    """
    if n == 1:
        end.push(begin.pop())
        return

    recursion_stack: Stack[Tuple[Stack[int], Stack[int], Stack[int], int, int]] = Stack()
    recursion_stack.push((begin, end, temp, n, 0))
    # positions:
    # 0: before first recursive call
    # 1: after first recursive call
    while len(recursion_stack._container) > 0:
        begin_curr, end_curr, temp_curr, n_curr, position = recursion_stack.pop()
        if position == 0:
            recursion_stack.push((begin_curr, end_curr, temp_curr, n_curr, 1))
            if n_curr == 2:
                temp_curr.push(begin_curr.pop())
            else:
                recursion_stack.push((begin_curr, temp_curr, end_curr, n_curr-1, 0))
        elif position == 1:
            end_curr.push(begin_curr.pop())
            if n_curr == 2:
                end_curr.push(temp_curr.pop())
            else:
                recursion_stack.push((temp_curr, end_curr, begin_curr, n_curr-1, 0))
    return

def hanoi_mtowers(towers: Tuple[Stack[int]], n: int) -> None:
    """
    Recursive hanoi solver for arbitrarily many towers.
    First two towers are begin and end. The rest are temp.
    """
    # THERE IS PROBABLY A SLIGHTLY MORE EFFICIENT WAY
    begin, end, temps = towers[0], towers[1], towers[2:]
    m = len(temps)
    if n <= m:
        for j in range(1, n):
            temps[j].push(begin.pop())
        end.push(begin.pop())
        for j in range(n-1, 0, -1):
            end.push(temps[j].pop())
    else:
        hanoi_mtowers((begin, temps[0], end) + temps[1:], n - m)
        hanoi_mtowers((begin, end) + temps, m)
        hanoi_mtowers((temps[0], end, begin) + temps[1:], n - m)

# ==== END MY SOLUTION ====

# listing 1.22
def hanoi(begin: Stack[int], end: Stack[int], temp: Stack[int], n: int) -> None:
    if n == 1:
        end.push(begin.pop())
    else:
        hanoi(begin, temp, end, n - 1)
        hanoi(begin, end, temp, 1)
        hanoi(temp, end, begin, n - 1)
        
if __name__ == '__main__':

    print("==== BOOK VERSION ====")
    # listing 1.21
    num_discs: int = 10
    
    tower_a: Stack[int] = Stack()
    tower_b: Stack[int] = Stack()
    tower_c: Stack[int] = Stack()
    for i in range(1, num_discs + 1):
        tower_a.push(i)

    print(f"{tower_a}  {tower_b}  {tower_c}       ")

    # listing 1.23
    hanoi(tower_a, tower_c, tower_b, num_discs)
    print(f"{tower_a}  {tower_b}  {tower_c}       ")

    print("==== MY NON-RECURSIVE VERSION ====")
    tower_a: Stack[int] = Stack()
    tower_b: Stack[int] = Stack()
    tower_c: Stack[int] = Stack()
    for i in range(1, num_discs + 1):
        tower_a.push(i)

    print(f"{tower_a}  {tower_b}  {tower_c}       ")
    hanoi_nonrecursive(tower_a, tower_c, tower_b, num_discs)
    print(f"{tower_a}  {tower_b}  {tower_c}       ")

    print("==== MY RECURSIVE MANY-TOWER VERSION ====")
    num_towers = 4
    towers: Tuple[Stack[int]] = tuple(Stack() for j in range(num_towers))
    for i in range(1, num_discs + 1):
        towers[0].push(i)

    print(f"{towers}      ")
    hanoi_mtowers(towers, num_discs)
    print(f"{towers}      ")
