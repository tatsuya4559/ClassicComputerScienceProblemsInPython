from __future__ import annotations
from typing import List, Optional
from general_search import bfs, Node, node_to_path


MAX_NUM = 3


class MCState:
    def __init__(self, missionaries: int, cannibals: int, boat: bool) -> None:
        self.wm: int = missionaries
        self.wc: int = cannibals
        self.em: int = MAX_NUM - self.wm
        self.ec: int = MAX_NUM - self.wc
        self.boat: bool = boat

    def __str__(self) -> str:
        boat_location = "西岸" if self.boat else "東岸"
        return f"""
        西岸の宣教師: {self.wm}, 食人種: {self.wc}
        東岸の宣教師: {self.em}, 食人種: {self.ec}
        ボートは{boat_location}
        """

    @property
    def is_legal(self) -> bool:
        if 0 < self.wm < self.wc or 0 < self.em < self.ec:
            return False
        return True

    def is_goal(self) -> bool:
        return self.is_legal and self.em == MAX_NUM and self.ec == MAX_NUM

    def successors(self) -> List[MCState]:
        sucs: List[MCState] = []
        if self.boat:
            if self.wm >= 2:
                sucs.append(MCState(self.wm - 2, self.wc, not self.boat))
            if self.wm >= 1:
                sucs.append(MCState(self.wm - 1, self.wc, not self.boat))
            if self.wc >= 2:
                sucs.append(MCState(self.wm, self.wc - 2, not self.boat))
            if self.wc >= 1:
                sucs.append(MCState(self.wm, self.wc - 1, not self.boat))
            if self.wm >= 1 and self.wc >= 1:
                sucs.append(MCState(self.wm - 1, self.wc - 1, not self.boat))
        else:
            if self.em >= 2:
                sucs.append(MCState(self.wm + 2, self.wc, not self.boat))
            if self.em >= 1:
                sucs.append(MCState(self.wm + 1, self.wc, not self.boat))
            if self.ec >= 2:
                sucs.append(MCState(self.wm, self.wc + 2, not self.boat))
            if self.ec >= 1:
                sucs.append(MCState(self.wm, self.wc + 1, not self.boat))
            if self.em >= 1 and self.ec >= 1:
                sucs.append(MCState(self.wm + 1, self.wc + 1, not self.boat))

        return [x for x in sucs if x.is_legal]


def display_solution(path: List[MCState]) -> None:
    for st in path:
        print(st)


def hr() -> None:
    print('--------------------------------------------------------------------------------')


def main() -> None:
    state: MCState = MCState(MAX_NUM, MAX_NUM, True)
    print(state)
    hr()
    solution: Optional[Node[MCState]] = bfs(state, MCState.is_goal, MCState.successors)
    if not solution:
        print("No solution is found...")
    else:
        path: List[MCState] = node_to_path(solution)
        display_solution(path)




if __name__ == "__main__":
    main()
