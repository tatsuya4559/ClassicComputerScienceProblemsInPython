from enum import Enum
from typing import List, NamedTuple, Callable, Optional
import random
from math import sqrt
from general_search import dfs, bfs, astar, node_to_path, Node


class Cell(str, Enum):
    EMPTY = " "
    BLOCKED = "X"
    START = "S"
    GOAL = "G"
    PATH = "*"


class MazeLocation(NamedTuple):
    row: int
    column: int

def euclidean_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = ml.column - goal.column
        ydist: int = ml.row - goal.row
        return sqrt(xdist ** 2 + ydist ** 2)
    return distance


def manhattan_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = ml.column - goal.column
        ydist: int = ml.row - goal.row
        return xdist + ydist
    return distance


class Maze:
    def __init__(
        self,
        rows: int = 10,
        columns: int = 10,
        sparseness: float = 0.2,
        start: MazeLocation = MazeLocation(0, 0),
        goal: MazeLocation = MazeLocation(9, 9),
    ) -> None:
        self._rows: int = rows
        self._columns: int = columns
        self.start: MazeLocation = start
        self.goal: MazeLocation = goal
        self._grid: List[List[Cell]] = [
            [Cell.EMPTY for c in range(columns)] for r in range(rows)
        ]
        self._randomly_fill(sparseness)
        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL

    def _randomly_fill(self, sparseness: float) -> None:
        for row in range(self._rows):
            for column in range(self._columns):
                if random.uniform(0, 1.0) < sparseness:
                    self._grid[row][column] = Cell.BLOCKED

    def __str__(self) -> str:
        output: str = ""
        for row in self._grid:
            output += "".join(c.value for c in row) + "\n"
        return output

    def is_goal(self, ml: MazeLocation) -> bool:
        return ml == self.goal

    def successors(self, ml: MazeLocation) -> List[MazeLocation]:
        locations: List[MazeLocation] = []
        if (
            ml.row + 1 < self._rows
            and self._grid[ml.row + 1][ml.column] != Cell.BLOCKED
        ):
            locations.append(MazeLocation(ml.row + 1, ml.column))
        if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.column))
        if (
            ml.column + 1 < self._columns
            and self._grid[ml.row][ml.column + 1] != Cell.BLOCKED
        ):
            locations.append(MazeLocation(ml.row, ml.column + 1))
        if ml.column - 1 >= 0 and self._grid[ml.row][ml.column - 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column - 1))
        return locations

    def mark(self, path: List[MazeLocation]) -> None:
        for ml in path:
            self._grid[ml.row][ml.column] = Cell.PATH
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

    def clear(self, path: List[MazeLocation]) -> None:
        for ml in path:
            self._grid[ml.row][ml.column] = Cell.EMPTY
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL


def hr() -> None:
    print('--------------------------------------------------------------------------------')


def main() -> None:
    m: Maze = Maze(30, 30, 0.4, MazeLocation(0, 0), MazeLocation(29,29))
    print(m)
    hr()
    solution1, count1 = dfs(m.start, m.is_goal, m.successors)
    if not solution1:
        print("No solution is found...")
    else:
        path1: List[MazeLocation] = node_to_path(solution1)
        m.mark(path1)
        print("dfs takes {count} steps. manhattan distance is {length}".format(count=count1, length=len(path1)))
        print(m)
        m.clear(path1)
        hr()
    solution2, count2 = bfs(m.start, m.is_goal, m.successors)
    if not solution2:
        print("No solution is found...")
    else:
        path2: List[MazeLocation] = node_to_path(solution2)
        print("dfs takes {count} steps. manhattan distance is {length}".format(count=count2, length=len(path2)))
        m.mark(path2)
        print(m)
        m.clear(path2)
        hr()
    solution3, count3 = astar(m.start, m.is_goal, m.successors, manhattan_distance(m.goal))
    if not solution3:
        print("No solution is found...")
    else:
        path3: List[MazeLocation] = node_to_path(solution3)
        print("dfs takes {count} steps. manhattan distance is {length}".format(count=count3, length=len(path3)))
        m.mark(path3)
        print(m)
        m.clear(path3)


if __name__ == "__main__":
    main()
