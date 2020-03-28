from __future__ import annotations
from typing import TypeVar, Generic, List, Tuple, Callable
from enum import Enum, auto
from random import choices, random
from heapq import nlargest
from statistics import mean
from chap5.chromosome import Chromosome

C = TypeVar("C", bound=Chromosome)


def _fitness_key_func(c: C) -> float:
    return c.fitness()


def _pick_roulette(population: List[C]) -> Tuple[C, C]:
    wheel: List[float] = [x.fitness() for x in population]
    return tuple(choices(population, weights=wheel, k=2))


def _pick_tournament(population) -> Tuple[C, C]:
    num_participants: int = len(population) // 2
    participants: List[C] = choices(population, k=num_participants)
    return tuple(nlargest(2, participants, key=_fitness_key_func))


class SelectionType(Enum):
    ROULETTE = _pick_roulette
    TOURNAMENT = _pick_tournament


class GeneticAlgorithm(Generic[C]):
    def __init__(
        self,
        initial_population: List[C],
        threshold: float,
        max_generations: int = 100,
        mutation_chance: float = 0.01,
        crossover_chance: float = 0.7,
        selection_type: SelectionType = SelectionType.TOURNAMENT,
    ) -> None:
        self._population: List[C] = initial_population
        self._threshold: float = threshold
        self._max_generations: int = max_generations
        self._mutation_chance: float = mutation_chance
        self._crossover_chance: float = crossover_chance
        self._pick_parent: Callable = selection_type

    def _reproduce_and_replace(self) -> None:
        new_population: List[C] = []
        while len(new_population) < len(self._population):
            parents: Tuple[C, C] = self._pick_parent(self._population)
            # 交叉
            if random() < self._crossover_chance:
                new_population.extend(parents[0].crossover(parents[1]))
            else:
                new_population.extend(parents)
        if len(new_population) > len(self._population):
            new_population.pop()
        self._population = new_population

    def _mutate(self) -> None:
        for individual in self._population:
            if random() < self._mutation_chance:
                individual.mutate()

    def run(self) -> C:
        best: C = max(self._population, key=_fitness_key_func)
        for generation in range(self._max_generations):
            if best.fitness() >= self._threshold:
                return best
            print(
                f"Generation {generation} Best {best.fitness()} Avg {mean(x.fitness() for x in self._population)}"
            )

            self._reproduce_and_replace()
            self._mutate()
            highest: C = max(self._population, key=_fitness_key_func)
            if highest.fitness() > best.fitness():
                best = highest
        return best
