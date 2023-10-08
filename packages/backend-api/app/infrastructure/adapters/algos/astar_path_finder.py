from typing import List, Tuple
from app.domain.ports.ipath_finder import IPathFinder
from app.domain.ports.igis_graph import IGisGraph
from geopy.distance import geodesic


class AStarPathFinder(IPathFinder):

    def __init__(self):
        pass

    def find_path(self, graph: IGisGraph, start: int, end: int) -> List[int]:
        open_list = set([start])
        closed_list = set([])
        g = {}
        g[start] = 0
        f = {}
        f[start] = self.__heuristic(graph, start, end)

        previous_nodes = {}
        while len(open_list) > 0:
            current_node = None
            for node in open_list:
                if current_node is None or f[node] < f[current_node]:
                    current_node = node

            if current_node == end:
                path = []
                while current_node in previous_nodes:
                    path.append(current_node)
                    current_node = previous_nodes[current_node]
                path.append(start)
                return path[::-1]

            open_list.remove(current_node)
            closed_list.add(current_node)

            for neighbor, weight in graph.get_neighbors(current_node):

                if neighbor in closed_list:
                    continue
                # Actualizado para usar el peso de la arista
                tentative_g = g[current_node] + weight

                if neighbor not in open_list:
                    open_list.add(neighbor)
                elif tentative_g >= g.get(neighbor, float('inf')):
                    continue

                previous_nodes[neighbor] = current_node
                g[neighbor] = tentative_g
                h = self.__heuristic(graph, neighbor, end)
                f[neighbor] = g[neighbor] + h

        return []

    def __heuristic(self, graph: IGisGraph, node1: int, node2: int) -> float:
        lat1, lon1 = graph.get_node_coordinates(node1)
        lat2, lon2 = graph.get_node_coordinates(node2)
        return geodesic((lat1, lon1), (lat2, lon2)).meters
