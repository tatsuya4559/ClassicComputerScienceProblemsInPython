from typing import List, Dict, Optional
from csp import CSP, Constraint


class SendMoreMoneyConstraint(Constraint[str, int]):
    def __init__(self, letters: List[str]):
        super().__init__(letters)
        self.letters = letters

    def satisfied(self, assignment: Dict[str, int]) -> bool:
        if (len(set(assignment.values()))) < len(assignment):
            return False
        if len(assignment) == len(self.letters):
            d: int = assignment["D"]
            e: int = assignment["E"]
            m: int = assignment["M"]
            n: int = assignment["N"]
            o: int = assignment["O"]
            r: int = assignment["R"]
            s: int = assignment["S"]
            y: int = assignment["Y"]
            send: int = 1000 * s + 100 * e + 10 * n + d
            more: int = 1000 * m + 100 * o + 10 * r + e
            money: int = 10000 * m + 1000 * o + 100 * n + 10 * e + y
            return send + more == money
        return True


if __name__ == "__main__":
    letters: List[str] = ["D", "E", "M", "N", "O", "R", "S", "Y"]
    posiible_digits: Dict[str, List[int]] = {}
    for l in letters:
        posiible_digits[l] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    posiible_digits["M"] = [1]
    csp: CSP[str, int] = CSP(letters, posiible_digits)
    csp.add_constraint(SendMoreMoneyConstraint(letters))
    solution: Optional[Dict[str, int]] = csp.backtracking_search()
    if solution is None:
        print("No solution found")
    else:
        print(solution)
        d: int = solution["D"]
        e: int = solution["E"]
        m: int = solution["M"]
        n: int = solution["N"]
        o: int = solution["O"]
        r: int = solution["R"]
        s: int = solution["S"]
        y: int = solution["Y"]
        send: int = 1000 * s + 100 * e + 10 * n + d
        more: int = 1000 * m + 100 * o + 10 * r + e
        money: int = 10000 * m + 1000 * o + 100 * n + 10 * e + y
        print(f"{send} + {more} = {money}")
