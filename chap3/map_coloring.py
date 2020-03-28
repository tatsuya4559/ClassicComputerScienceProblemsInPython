from csp import CSP, Constraint
from typing import Dict, List, Optional
from pprint import pprint


class MapColoringConstraint(Constraint[str, str]):
    def __init__(self, place1: str, place2: str) -> None:
        super().__init__([place1, place2])
        self.place1: str = place1
        self.place2: str = place2

    def satisfied(self, assignment: Dict[str, str]) -> bool:
        if self.place1 not in assignment or self.place2 not in assignment:
            return True
        return assignment[self.place1] != assignment[self.place2]


if __name__ == "__main__":
    WA: str = "Western Australia"
    NT: str = "Northern Territory"
    SA: str = "South Australia"
    QL: str = "Queensland"
    NW: str = "New South Wales"
    VA: str = "Victoria"
    TM: str = "Tasmania"
    variables: List[str] = [WA, NT, SA, QL, NW, VA, TM]
    domains: Dict[str, List[str]] = {
        variable: ["red", "green", "blue"] for variable in variables
    }
    csp: CSP[str, str] = CSP(variables, domains)
    csp.add_constraint(MapColoringConstraint(WA, NT))
    csp.add_constraint(MapColoringConstraint(WA, SA))
    csp.add_constraint(MapColoringConstraint(SA, NT))
    csp.add_constraint(MapColoringConstraint(QL, NT))
    csp.add_constraint(MapColoringConstraint(QL, SA))
    csp.add_constraint(MapColoringConstraint(QL, NW))
    csp.add_constraint(MapColoringConstraint(NW, SA))
    csp.add_constraint(MapColoringConstraint(VA, SA))
    csp.add_constraint(MapColoringConstraint(VA, NW))
    csp.add_constraint(MapColoringConstraint(VA, TM))
    solution: Optional[Dict[str, str]] = csp.backtracking_search()
    if not solution:
        print("solution not found")
    else:
        pprint(solution)
