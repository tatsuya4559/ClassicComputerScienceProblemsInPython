from typing import List, Generic, TypeVar, Optional
from chap2.general_search import bfs, Node, node_to_path
from city import City
from edge import Edge

V = TypeVar("V")


class Graph(Generic[V]):
    def __init__(self, vertices: List[V] = []) -> None:
        self._vertices: List[V] = vertices  # 節点
        self._edges: List[List[Edge]] = [[] for _ in vertices]  # 辺

    @property
    def vertex_count(self) -> int:
        return len(self._vertices)

    @property
    def edge_count(self) -> int:
        return sum(map(len, self._edges))

    def add_vertex(self, vertex: V) -> int:
        """追加した節点のインデックスを返す"""
        self._vertices.append(vertex)
        self._edges.append([])
        return self.vertex_count - 1

    def add_edge(self, edge: Edge) -> None:
        self._edges[edge.u].append(edge)
        self._edges[edge.v].append(edge.reversed())

    def add_egde_by_indices(self, u: int, v: int) -> None:
        self.add_edge(Edge(u, v))

    def add_edge_by_vertices(self, first: V, second: V) -> None:
        u: int = self.index_of(first)
        v: int = self.index_of(second)
        self.add_egde_by_indices(u, v)

    def vertex_at(self, index: int) -> V:
        return self._vertices[index]

    def index_of(self, vertex: V) -> int:
        return self._vertices.index(vertex)

    def neighbors_for_index(self, index: int) -> List[V]:
        return [self.vertex_at(edge.v) for edge in self.edges_for_index(index)]

    def neighbors_for_vertex(self, vertex: V) -> List[V]:
        return self.neighbors_for_index(self.index_of(vertex))

    def edges_for_index(self, index: int) -> List[Edge]:
        return self._edges[index]

    def edges_for_vertex(self, vertex: V) -> List[Edge]:
        return self.edges_for_index(self.index_of(vertex))

    def __str__(self) -> str:
        return "\n".join(
            f"{self.vertex_at(i)} -> {self.neighbors_for_index(i)}"
            for i in range(self.vertex_count)
        )


if __name__ == "__main__":
    city_graph: Graph[City] = Graph(list(City))

    city_graph.add_edge_by_vertices(City.SEA, City.CHI)
    city_graph.add_edge_by_vertices(City.SEA, City.SFO)
    city_graph.add_edge_by_vertices(City.SFO, City.RVS)
    city_graph.add_edge_by_vertices(City.SFO, City.LAX)
    city_graph.add_edge_by_vertices(City.LAX, City.RVS)
    city_graph.add_edge_by_vertices(City.LAX, City.PHX)
    city_graph.add_edge_by_vertices(City.RVS, City.PHX)
    city_graph.add_edge_by_vertices(City.RVS, City.CHI)
    city_graph.add_edge_by_vertices(City.PHX, City.DAL)
    city_graph.add_edge_by_vertices(City.PHX, City.HOU)
    city_graph.add_edge_by_vertices(City.DAL, City.CHI)
    city_graph.add_edge_by_vertices(City.DAL, City.ATL)
    city_graph.add_edge_by_vertices(City.DAL, City.HOU)
    city_graph.add_edge_by_vertices(City.HOU, City.ATL)
    city_graph.add_edge_by_vertices(City.HOU, City.MIA)
    city_graph.add_edge_by_vertices(City.ATL, City.CHI)
    city_graph.add_edge_by_vertices(City.ATL, City.DCA)
    city_graph.add_edge_by_vertices(City.ATL, City.MIA)
    city_graph.add_edge_by_vertices(City.MIA, City.DCA)
    city_graph.add_edge_by_vertices(City.CHI, City.DTW)
    city_graph.add_edge_by_vertices(City.DTW, City.BOS)
    city_graph.add_edge_by_vertices(City.DTW, City.DCA)
    city_graph.add_edge_by_vertices(City.DTW, City.NYK)
    city_graph.add_edge_by_vertices(City.BOS, City.NYK)
    city_graph.add_edge_by_vertices(City.NYK, City.PHL)
    city_graph.add_edge_by_vertices(City.PHL, City.DCA)

    bfs_result: Optional[Node[City]] = bfs(
        City.BOS, lambda x: x == City.MIA, city_graph.neighbors_for_vertex
    )
    if bfs_result is None:
        print("not found")
    else:
        path: List[City] = node_to_path(bfs_result)
        print(path)
