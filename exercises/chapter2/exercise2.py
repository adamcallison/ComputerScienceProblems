from __future__ import annotations

# EXERCISE 2 IS TO ADD COUNTERS TO THE VARIOUS SEARCH FUNCTIONS
# SO PART OF MY SOLUTION IS INTERSPERSED THROUGHOUT THE FUNCTIONS

from enum import Enum
from typing import NamedTuple, List, Generic, TypeVar, Optional, Deque, \
    Tuple, Union
import random
from heapq import heappush, heappop

T = TypeVar('T')

# from listing 2.10
class Cell(str, Enum):
    EMPTY = " "
    BLOCKED = "X"
    START = "S"
    GOAL = "G"
    PATH = "*"

# from listing 2.11
class MazeLocation(NamedTuple):
    row: int
    column: int

# from listings 2.12, 2.13, 2.14, and 2.15
class Maze:
    def __init__(self, rows: int = 10, columns: int = 10, \
        sparseness: float = 0.2, start: MazeLocation = MazeLocation(0, 0), \
        goal: MazeLocation = MazeLocation(9, 9)) -> None:
        # initialize basic instance variables
        self._rows: int = rows
        self._columns: int = columns
        self.start: MazeLocation = start
        self.goal: MazeLocation = goal
        # fill the grid with empty cells
        self._grid: List[List[Cell]] = [[Cell.EMPTY for c in range(columns)] \
            for r in range(rows)]
        # populate the grid with blocked cells
        self._randomly_fill(rows, columns, sparseness)
        # fill the start and goal locations in
        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL

    def _randomly_fill(self, rows: int, columns: int, sparseness: float):
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0, 1.0) < sparseness:
                    self._grid[row][column] = Cell.BLOCKED

    def __str__(self) -> str:
        output: str = ""
        for row in self._grid:
            output += "".join([c.value for c in row]) + "\n"
        return output

    def goal_test(self, ml: MazeLocation) -> bool:
        return ml == self.goal

    def successors(self, ml: MazeLocation) -> List[MazeLocation]:
        locations: List[MazeLocation] = []
        if ml.row + 1 < self._rows and self._grid[ml.row + 1][ml.column] != \
            Cell.BLOCKED:
            locations.append(MazeLocation(ml.row + 1, ml.column))
        if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.column] != \
            Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.column))
        if ml.column + 1 < self._columns and self._grid[ml.row][ml.column + 1] \
            != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column + 1))
        if ml.column - 1 >= 0 and self._grid[ml.row][ml.column - 1] != \
            Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column - 1))
        return locations

    # from listing 2.20
    def mark(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.PATH
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

    def clear(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.EMPTY
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

# from listing 2.16
class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container # not is true for empty container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    def __repr__(self) -> str:
        return repr(self._container)

# from listing 2.17
class Node(Generic[T]):
    def __init__(self, state: T, parent: Optional[Node], cost: float = 0.0, \
        heuristic: float = 0.0) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other: Node) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

# from listing 2.18
def dfs(initial: T, goal_test: Callable[[T], bool], successors: \
    Callable[[T], List[T]], count_states: bool = False) -> \
    Union[Optional[Node[T]], Tuple[Optional[Node[T]], int]]:

    # My solution: added in count_states arg

    # frontier is where we've yet to go
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))
    # explored is where we've been
    explored: Set[T] = {initial}
    # keep going while there is more to explore

    #my solution:
    count: int = 0
    ##############

    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state

        #my solution:
        count += 1
        ##############

        # if we found the goal, we're done
        if goal_test(current_state):

            # My solution: added returning count
            if count_states:
                return current_node, count
            else:
                return current_node

        # check where we can go next and haven't explored
        for child in successors(current_state):
            if child in explored: # skip children we already explored
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))

    # went through everything and never found goal:
    # My solution: added returning count
    if count_states:
        return None, count
    else:
        return None


# from listing 2.19
def node_to_path(node: Node[T]) -> List[T]:
    path: List[T] = [node.state]
    # work backwards from end to front
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path

# from listing 2.22
class Queue(Generic[T]):
    def __init__(self) -> None:
        self._container: Deque[T] = Deque()

    @property
    def empty(self) -> bool:
        return not self._container # not is true for empty container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.popleft() # FIFO

    def __repr__(self) -> str:
        return repr(self._container)

# from listing 2.23
def bfs(initial: T, goal_test: Callable[[T], bool], successors: \
    Callable[[T], List[T]], count_states: bool = False) -> \
    Union[Optional[Node[T]], Tuple[Optional[Node[T]], int]]:

    # My solution: added in count_states arg

    # frontier is where we've yet to go
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))
    # explored is where we've been
    explored: Set[T] = {initial}
    # keep going while there is more to explore

    #my solution:
    count: int = 0
    ##############

    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state

        #my solution:
        count += 1
        ##############

        # if we found the goal, we're done
        if goal_test(current_state):

            # My solution: added returning count
            if count_states:
                return current_node, count
            else:
                return current_node

        # check where we can go next and haven't explored
        for child in successors(current_state):
            if child in explored: # skip children we already explored
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))

    # went through everything and never found goal:
    # My solution: added returning count
    if count_states:
        return None, count
    else:
        return None

# from listing 2.25
class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container # not is true for empty container

    def push(self, item: T) -> None:
        heappush(self._container, item) # in by priority

    def pop(self) -> T:
        return heappop(self._container) # out by priority

    def __repr__(self) -> str:
        return repr(self._container)

# from listing 2.26
def euclidean_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = ml.column - goal.column
        ydist: int = ml.row - goal.row
        return sqrt((xdist * xdist) + (ydist * ydist))
    return distance

# from listing 2.27
def manhattan_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = abs(ml.column - goal.column)
        ydist: int = abs(ml.row - goal.row)
        return (xdist + ydist)
    return distance

# from listing 2.28
def astar(initial: T, goal_test: Callable[[T], bool], \
    successors: Callable[[T], List[T]], heuristic: Callable[[T], float], \
    count_states: bool = False) -> \
    Union[Optional[Node[T]], Tuple[Optional[Node[T]], int]]:

    # My solution: added in count_states arg)

    # frontier is where we've yet to go
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0.0, heuristic(initial)))
    # explored is where we've been
    explored: Dict[T, float] = {initial: 0.0}
    # keep going while there is more to explore

    #my solution:
    count: int = 0
    ##############

    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state

        #my solution:
        count += 1
        ##############

        # if we found the goal, we're done
        if goal_test(current_state):

            # My solution: added returning count
            if count_states:
                return current_node, count
            else:
                return current_node

        # check where we can go next and haven't explored
        for child in successors(current_state):

            new_cost: float = current_node.cost + 1 
            #    1 assumes a grid, need a cost function for more sophisticated 
            # apps

            if child not in explored or explored[child] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node, new_cost, \
                    heuristic(child)))

    # went through everything and never found goal:
    # My solution: added returning count
    if count_states:
        return None, count
    else:
        return None

if __name__ == "__main__":

    print('===== Testing DFS without count =====')
    # from listing 2.21
    m: Maze = Maze()
    print(m)
    solution1: Optional[Node[MazeLocation]] = dfs(m.start, m.goal_test, \
        m.successors)
    if solution1 is None:
        print("No solution found using depth-first search!")
    else:
        path1: List[MazeLocation] = node_to_path(solution1)
        m.mark(path1)
        print(m)
        m.clear(path1)
    print('=======================')
    print('===== Testing BFS without count =====')
    # from listing 2.24
    solution2: Optional[Node[MazeLocation]] = bfs(m.start, m.goal_test, 
        m.successors)
    if solution2 is None:
        print("No solution found using breadth-first search!")
    else:
        path2: List[MazeLocation] = node_to_path(solution2)
        m.mark(path2)
        print(m)
        m.clear(path2)
    print('=======================')
    print('===== Testing Astar without count =====')
    # from listing 2.29
    distance: Callable[[MazeLocation], float] = manhattan_distance(m.goal)
    solution3: Optional[Node[MazeLocation]] = astar(m.start, m.goal_test, \
        m.successors, distance)
    if solution3 is None:
        print("No solution found using A*!")
    else:
        path3: List[MazeLocation] = node_to_path(solution3)
        m.mark(path3)
        print(m)
        m.clear(path3)
    print('=======================')
    print('===== Testing DFS with count =====')
    solution4: Optional[Node[MazeLocation]]
    count4: int
    solution4, count4 = dfs(m.start, m.goal_test, m.successors, \
        count_states=True)
    if solution1 is None:
        print("No solution found using depth-first search!")
    else:
        path4: List[MazeLocation] = node_to_path(solution4)
        m.mark(path4)
        print(m)
        m.clear(path4)
    print(f"Visited {count4} states.")
    print('=======================')
    print('===== Testing BFS with count =====')
    solution5: Optional[Node[MazeLocation]]
    count5: int
    solution5, count5 = bfs(m.start, m.goal_test, m.successors, \
        count_states=True)
    if solution5 is None:
        print("No solution found using breadth-first search!")
    else:
        path5: List[MazeLocation] = node_to_path(solution5)
        m.mark(path5)
        print(m)
        m.clear(path5)
    print(f"Visited {count5} states.")
    print('=======================')
    print('===== Testing Astar with count =====')
    distance: Callable[[MazeLocation], float] = manhattan_distance(m.goal)
    solution6: Optional[Node[MazeLocation]]
    count6: int
    solution6, count6 = astar(m.start, m.goal_test, m.successors, distance, \
        count_states=True)
    if solution6 is None:
        print("No solution found using A*!")
    else:
        path6: List[MazeLocation] = node_to_path(solution6)
        m.mark(path6)
        print(m)
        m.clear(path6)
    print(f"Visited {count6} states.")
    print('=======================')

    print("~~~Exercise1 solution, statistics~~~")
    counts4: List[int] = []
    counts5: List[int] = []
    counts6: List[int] = []
    for j in range(100):
        m: Maze = Maze()
        solution4, count4 = dfs(m.start, m.goal_test, m.successors, \
        count_states=True)
        solution5, count5 = bfs(m.start, m.goal_test, m.successors, \
        count_states=True)
        distance: Callable[[MazeLocation], float] = manhattan_distance(m.goal)
        solution6, count6 = astar(m.start, m.goal_test, m.successors, distance, \
        count_states=True)
        counts4.append(count4)
        counts5.append(count5)
        counts6.append(count6)
    print(f"Mean states visited for dfs is {sum(counts4)/len(counts4)}")
    print(f"Mean states visited for bfs is {sum(counts5)/len(counts5)}")
    print(f"Mean states visited for astar is {sum(counts6)/len(counts6)}")
