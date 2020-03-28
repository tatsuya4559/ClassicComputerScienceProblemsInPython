from typing import List, TypeVar, Optional, Set
from weighted_graph import WeightedGraph
from weighted_edge import WeightedEdge
from chap2.general_search import PriorityQueue
from city import City

V = TypeVar("V")
WeightedPath = List[WeightedEdge]


def total_weight(wp: WeightedPath) -> float:
    return sum(e.weight for e in wp)


def mst(wg: WeightedGraph, start: int = 0) -> Optional[WeightedPath]:
    if start > (wg.vertex_count - 1) or start < 0:
        return None
    result: WeightedPath = []
    pq: PriorityQueue[WeightedEdge] = PriorityQueue()
    visited: Set[int] = set()

    def visit(index: int) -> None:
        visited.add(index)
        for edge in wg.edges_for_index(index):
            if edge.v not in visited:
                pq.push(edge)

    visit(start)
    while not pq.is_empty():
        edge = pq.pop()
        if edge.v in visited:
            continue
        result.append(edge)
        visit(edge.v)
    return result


def print_weighted_path(wg: WeightedGraph, wp: WeightedPath) -> None:
    for edge in wp:
        print(
            f"{wg.vertex_at(edge.u).value} {edge.weight}> {wg.vertex_at(edge.v).value}"
        )
    print(f"Total weight: {total_weight(wp)}")


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

    result: Optional[WeightedPath] = mst(city_graph2)
    if result is None:
        print("not found")
    else:
        print_weighted_path(city_graph2, result)
