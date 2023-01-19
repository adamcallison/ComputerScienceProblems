# listing 1.3
def fib2(n: int) -> int:
    if n < 2: # base case
        return n
    return fib2(n - 2) + fib2(n - 1)
    # recursive case

# listing 1.5
from typing import Dict
memo: Dict[int, int] = {0: 0, 1: 1} # our base cases
def fib3(n: int) -> int:
    if n not in memo:
        memo[n] = fib3(n - 1) + fib3(n - 2)
    return memo[n]

# listing 1.7
from functools import lru_cache
@lru_cache(maxsize=None)
def fib4(n: int) -> int: # same definition as fib2()
    if n < 2: # base case
        return n
    return fib4(n - 2) + fib4(n - 1) # recursive case

def fib5(n: int) -> int:
    if n == 0: return n # special case
    last: int = 0 # initially set to fib(0)
    next: int = 1 # initially set to fib(1)
    for _ in range(1, n):
        last, next = next, last + next
    return next

from typing import Generator
def fib6(n: int) -> Generator[int, None, None]:
    yield 0 # special case
    if n > 0: yield 1 # special case
    last: int = 0 # initially set to fib(0)
    next: int = 1 # initially set to fib(1)
    for _ in range(1, n):
        last, next = next, last + next
        yield next # main generation step

from itertools import product
from typing import List
solution_stored: List[int] = [0, 1]
def solution(n: int) -> int:
    global solution_stored
    if len(solution_stored) >= n+1:
        pass
    else:
        for _ in range(2, n+1):
            solution_stored.append(solution_stored[-2]+solution_stored[-1])
    return solution_stored[n]

if __name__ == '__main__':
    from time import time

    stime = time()
    nvals = (list(range(0, 50))+list(range(100, 50, -1)))
    for n in nvals:
        fib3(n)
    etime = time()
    print(f"fib3: {1e6*(etime-stime)/len(nvals)}ms per call on average.       ")

    stime = time()
    nvals = (list(range(0, 50))+list(range(100, 50, -1)))
    for n in nvals:
        fib4(n)
    etime = time()
    print(f"fib4: {1e6*(etime-stime)/len(nvals)}ms per call on average.       ")

    stime = time()
    nvals = (list(range(0, 50))+list(range(100, 50, -1)))
    for n in nvals:
        fib5(n)
    etime = time()
    print(f"fib5: {1e6*(etime-stime)/len(nvals)}ms per call on average.       ")

    stime = time()
    nvals = (list(range(0, 50))+list(range(100, 50, -1)))
    for n in nvals:
        solution(n)
    etime = time()
    print(f"my solution: {1e6*(etime-stime)/len(nvals)}ms per call on average.       ")
    



