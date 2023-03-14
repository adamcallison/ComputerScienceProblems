from exercises.chapter2 import exercise2

import pytest
from time import time
import random

@pytest.mark.parametrize("testid", range(100))
def test_astar(testid):
    counts_bfs, counts_astar = [], []
    for j in range(100):
        m = exercise2.Maze()
        solution_bfs, count_bfs = exercise2.bfs(m.start, m.goal_test, \
        m.successors, count_states=True)
        distance = exercise2.manhattan_distance(m.goal)
        solution_astar, count_astar = exercise2.astar(m.start, m.goal_test, \
        m.successors, distance, count_states=True)
        counts_bfs.append(count_bfs)
        counts_astar.append(count_astar)
    mean_astar = sum(counts_astar)/len(counts_astar)
    mean_bfs = sum(counts_bfs)/len(counts_bfs)
    assert mean_astar < mean_bfs

