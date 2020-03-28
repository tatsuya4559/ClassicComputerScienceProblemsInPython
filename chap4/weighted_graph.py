from typing import List, TypeVar, Tuple
from weighted_edge import WeightedEdge
from city import City
from graph import Graph

V = TypeVar("V")


class WeightedGraph(Graph[V]):
    def __init__(self, vertices: List[V] = []) -> None:
        self._vertices: List[V] = vertices  # 節点
        self._edges: List[List[WeightedEdge]] = [[] for _ in vertices]  # 辺

    def add_egde_by_indices(self, u: int, v: int, weight: float) -> None:
        edge: WeightedEdge = WeightedEdge(u, v, weight)
        self.add_edge(edge)

    def add_edge_by_vertices(self, first: V, second: V, weight: float) -> None:
        u: int = self.index_of(first)
        v: int = self.index_of(second)
        self.add_egde_by_indices(u, v, weight)

    def neighbors_for_index_with_weights(self, index: int) -> List[Tuple[V, float]]:
        return [
            (self.vertex_at(edge.v), edge.weight)
            for edge in self.edges_for_index(index)
        ]

    def __str__(self) -> str:
        return "\n".join(
            f"{self.vertex_at(i)} -> {self.neighbors_for_index_with_weights(i)}"
            for i in range(self.vertex_count)
        )

