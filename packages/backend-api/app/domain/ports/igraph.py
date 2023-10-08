from abc import ABC, abstractmethod
from typing import List, Tuple
from networkx.algorithms.shortest_paths.astar import astar_path


class IGraph(ABC):
    @abstractmethod
    def add_node(self, id: int, lat: float, lon: float):
        pass

    @abstractmethod
    def add_edge(self, node1_id: int, node2_id: int, weight: float):
        pass

    @abstractmethod
    def get_node_coordinates(self, node_id: int) -> Tuple[float, float]:
        pass

    @abstractmethod
    def get_neighbors(self, node_id: int) -> List[Tuple[int, float]]:
        pass

    @abstractmethod
    def create_graph(self, node_id: int) -> 'IGraph':
        pass
