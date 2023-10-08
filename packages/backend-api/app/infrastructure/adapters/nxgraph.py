from typing import List, Tuple
from app.infrastructure.dto.node_dto import NodeDTO
from networkx import Graph as NXGraph
from app.domain.ports.igraph import IGraph


class NXGraph(IGraph):
    def __init__(self):
        self.graph = NXGraph()

    def add_node(self, id: int, lat: float, lon: float):  # Removed @abstractmethod
        self.graph.add_node(id, lat=lat, lon=lon)

    def add_edge(self, node1_id: int, node2_id: int, weight: float):  # Removed @abstractmethod
        self.graph.add_edge(node1_id, node2_id, weight=weight)

    def get_neighbors(self, node_id: int) -> List[Tuple[int, float]]:
        neighbors = [(neighbor, self.graph[node_id][neighbor].get('weight', 1.0))
                     for neighbor in self.graph.neighbors(node_id)]
        return neighbors

    @classmethod
    def create_graph(cls, nodes: List[NodeDTO]) -> 'NXGraph':
        adapter = cls()
        for node in nodes:
            adapter.add_node(node.id, node.lat, node.lon)
        return adapter
