from __future__ import annotations
from typing import Tuple, List
from chap5.chromosome import Chromosome
from chap5.genetic_algorithm import GeneticAlgorithm, SelectionType
from random import shuffle, sample
from copy import deepcopy


class SendMoreMoney2(Chromosome):
    def __init__(self, letters: List[str]) -> None:
        self.letters: List[str] = letters

    def fitness(self) -> float:
        return 1 / (abs(self.money - self.send - self.more) + 1)

    @classmethod
    def random_instance(cls) -> SendMoreMoney2:
        letters: List[str] = ["D", "E", "M", "N", "O", "R", "S", "Y", "", ""]
        shuffle(letters)
        return SendMoreMoney2(letters)

    def crossover(self, other: SendMoreMoney2) -> Tuple[SendMoreMoney2, SendMoreMoney2]:
        child1: SendMoreMoney2 = deepcopy(self)
        child2: SendMoreMoney2 = deepcopy(other)
        idx1, idx2 = sample(range(len(self.letters)), k=2)
        l1, l2 = child1.letters[idx1], child2.letters[idx2]
        child1.letters[child1.letters.index(l2)], child1.letters[idx2] = (
            child1.letters[idx2],
            l2,
        )
        child2.letters[child2.letters.index(l1)], child2.letters[idx1] = (
            child2.letters[idx1],
            l1,
        )
        return child1, child2

    def mutate(self) -> None:
        idx1, idx2 = sample(range(len(self.letters)), k=2)
        self.letters[idx1], self.letters[idx2] = self.letters[idx2], self.letters[idx1]

    @property
    def send(self) -> int:
        s: int = self.letters.index("S")
        e: int = self.letters.index("E")
        n: int = self.letters.index("N")
        d: int = self.letters.index("D")
        return s * 1000 + e * 100 + n * 10 + d

    @property
    def more(self) -> int:
        m: int = self.letters.index("M")
        o: int = self.letters.index("O")
        r: int = self.letters.index("R")
        e: int = self.letters.index("E")
        return m * 1000 + o * 100 + r * 10 + e

    @property
    def money(self) -> int:
        m: int = self.letters.index("M")
        o: int = self.letters.index("O")
        n: int = self.letters.index("N")
        e: int = self.letters.index("E")
        y: int = self.letters.index("Y")
        return m * 10000 + o * 1000 + n * 100 + e * 10 + y

    def __str__(self) -> str:
        send = self.send
        more = self.more
        money = self.money
        diff: int = abs(money - send - more)
        return f"{send} + {more} = {money} Diff: {diff}"


if __name__ == "__main__":
    initial_population: List[SendMoreMoney2] = [
        SendMoreMoney2.random_instance() for _ in range(1000)
    ]
    ga: GeneticAlgorithm[SendMoreMoney2] = GeneticAlgorithm(
        initial_population=initial_population,
        threshold=1.0,
        max_generations=3,
        mutation_chance=0.2,
        crossover_chance=0.7,
        selection_type=SelectionType.TOURNAMENT,
    )
    result: SendMoreMoney2 = ga.run()
    print(result)

