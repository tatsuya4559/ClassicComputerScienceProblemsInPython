from __future__ import annotations
from typing import TypeVar, List, Optional, Tuple, Dict
from collections import deque
from dataclasses import dataclass
from mst import WeightedPath, print_weighted_path
from weighted_graph import WeightedGraph
from weighted_edge import WeightedEdge
from chap2.general_search import PriorityQueue
from city import City

V = TypeVar("V")


@dataclass
class DijkstraNode:
    vertex: int
    distance: float

    def __lt__(self, other: DijkstraNode) -> bool:
        return self.distance < other.distance

    def __eq__(self, other: DijkstraNode) -> bool:
        return self.distance == other.distance


def dijkstra(
    wg: WeightedGraph[V], root: V
) -> Tuple[List[Optional[float]], Dict[int, WeightedEdge]]:
    first: int = wg.index_of(root)
    distances: List[Optional[float]] = [None for _ in range(wg.vertex_count)]
    distances[first] = 0
    path_dict: Dict[int, WeightedEdge] = {}
    pq: PriorityQueue[DijkstraNode] = PriorityQueue()
    pq.push(DijkstraNode(first, distances[first]))

    while not pq.is_empty():
        dn: DijkstraNode = pq.pop()
        u: int = dn.vertex
        dist_u: float = dn.distance
        for we in wg.edges_for_index(u):
            dist_v: Optional[float] = distances[we.v]
            if dist_v is None or dist_v > we.weight + dist_u:
                distances[we.v] = we.weight + dist_u
                path_dict[we.v] = we
                pq.push(DijkstraNode(we.v, distances[we.v]))

    return distances, path_dict


def distance_array_to_vertex_dict(
    wg: WeightedGraph[V], distances: List[Optional[float]]
) -> Dict[V, Optional[float]]:
    return {wg.vertex_at(index): distance for index, distance in enumerate(distances)}


def path_dict_to_path(
    start: int, end: int, path_dict: Dict[int, WeightedEdge]
) -> WeightedPath:
    if not path_dict:
        return []
    edge_path = deque()
    edge: WeightedEdge = path_dict[end]
    edge_path.appendleft(edge)
    while edge.u != start:
        edge = path_dict[edge.u]
        edge_path.appendleft(edge)
    return list(edge_path)


if __name__ == "__main__":
    city_graph2: WeightedGraph[City] = WeightedGraph(list(City))

    city_graph2.add_edge_by_vertices(City.SEA, City.CHI, 1737)
    city_graph2.add_edge_by_vertices(City.SEA, City.SFO, 678)
    city_graph2.add_edge_by_vertices(City.SFO, City.RVS, 386)
    city_graph2.add_edge_by_vertices(City.SFO, City.LAX, 348)
    city_graph2.add_edge_by_vertices(City.LAX, City.RVS, 50)
    city_graph2.add_edge_by_vertices(City.LAX, City.PHX, 357)
    city_graph2.add_edge_by_vertices(City.RVS, City.PHX, 307)
    city_graph2.add_edge_by_vertices(City.RVS, City.CHI, 1704)
    city_graph2.add_edge_by_vertices(City.PHX, City.DAL, 887)
    city_graph2.add_edge_by_vertices(City.PHX, City.HOU, 1015)
    city_graph2.add_edge_by_vertices(City.DAL, City.CHI, 805)
    city_graph2.add_edge_by_vertices(City.DAL, City.ATL, 721)
    city_graph2.add_edge_by_vertices(City.DAL, City.HOU, 225)
    city_graph2.add_edge_by_vertices(City.HOU, City.ATL, 702)
    city_graph2.add_edge_by_vertices(City.HOU, City.MIA, 968)
    city_graph2.add_edge_by_vertices(City.ATL, City.CHI, 588)
    city_graph2.add_edge_by_vertices(City.ATL, City.DCA, 543)
    city_graph2.add_edge_by_vertices(City.ATL, City.MIA, 604)
    city_graph2.add_edge_by_vertices(City.MIA, City.DCA, 923)
    city_graph2.add_edge_by_vertices(City.CHI, City.DTW, 238)
    city_graph2.add_edge_by_vertices(City.DTW, City.BOS, 613)
    city_graph2.add_edge_by_vertices(City.DTW, City.DCA, 396)
    city_graph2.add_edge_by_vertices(City.DTW, City.NYK, 482)
    city_graph2.add_edge_by_vertices(City.BOS, City.NYK, 190)
    city_graph2.add_edge_by_vertices(City.NYK, City.PHL, 81)
    city_graph2.add_edge_by_vertices(City.PHL, City.DCA, 123)

    distances, path_dict = dijkstra(city_graph2, City.LAX)
    name_distance: Dict[str, Optional[float]] = distance_array_to_vertex_dict(
        city_graph2, distances
    )
    print("Distance from LA:")
    for k, v in name_distance.items():
        print(f"=> {k.value}: {v}")
    print("")

    print("Shortest path from LA to Boston:")
    path: WeightedPath = path_dict_to_path(
        city_graph2.index_of(City.LAX), city_graph2.index_of(City.BOS), path_dict
    )
    print_weighted_path(city_graph2, path)
