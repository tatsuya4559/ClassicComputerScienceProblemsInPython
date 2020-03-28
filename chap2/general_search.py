from __future__ import annotations
from collections import deque
from heapq import heappop, heappush
from typing import Generic, TypeVar, Optional, Callable, Set, Deque, List, Dict


T = TypeVar("T")


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._stack: Deque[T] = deque()

    def push(self, item: T) -> None:
        self._stack.append(item)

    def pop(self) -> T:
        return self._stack.pop()

    def is_empty(self) -> bool:
        return len(self._stack) == 0

    def __repr__(self) -> str:
        return repr(self._stack)


class Queue(Generic[T]):
    def __init__(self) -> None:
        self._queue: Deque[T] = deque()

    def push(self, item: T) -> None:
        self._queue.append(item)

    def pop(self) -> T:
        return self._queue.popleft()

    def is_empty(self) -> bool:
        return len(self._queue) == 0

    def __repr__(self) -> str:
        return repr(self._queue)


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    def push(self, item: T) -> None:
        heappush(self._container, item)

    def pop(self) -> T:
        return heappop(self._container)

    def is_empty(self) -> bool:
        return not self._container

    def __repr__(self) -> str:
        return repr(self._container)


class Node(Generic[T]):
    def __init__(
        self,
        state: T,
        parent: Optional[Node],
        cost: float = 0.0,
        heuristic: float = 0.0,
    ) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other: Node) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def dfs(
    initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]
) -> Optional[Node[T]]:
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))
    explored: Set[T] = {initial}

    while not frontier.is_empty():
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        if goal_test(current_state):
            return current_node
        for child in successors(current_state):
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None


def bfs(
    initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]
) -> Optional[Node[T]]:
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))
    explored: Set[T] = {initial}

    while not frontier.is_empty():
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        if goal_test(current_state):
            return current_node
        for child in successors(current_state):
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None


def astar(
    initial: T,
    goal_test: Callable[[T], bool],
    successors: Callable[[T], List[T]],
    heuristic: Callable[[T], float],
) -> Optional[Node[T]]:
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0.0, heuristic(initial)))
    explored: Dict[T, float] = {initial: 0.0}

    while not frontier.is_empty():
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        if goal_test(current_state):
            return current_node
        for child in successors(current_state):
            new_cost: float = current_node.cost + 1
            if child in explored and explored[child] <= new_cost:
                continue
            explored[child] = new_cost
            frontier.push(Node(child, current_node, new_cost, heuristic(child)))
    return None


def node_to_path(node: Node[T]) -> List[T]:
    path: List[T] = [node.state]
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path
