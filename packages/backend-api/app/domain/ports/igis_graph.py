from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Optional


class IGisGraph(ABC):

    @abstractmethod
    def add_node(self, id: int, lat: float, lon: float) -> None:
        pass

    @abstractmethod
    def add_edge(self, node1_id: int, node2_id: int, weight: float) -> None:
        pass

    @abstractmethod
    def get_neighbors(self, node_id: int) -> List[Tuple[int, float]]:
        pass

    @abstractmethod
    def get_node_coordinates(self, node_id: int) -> Tuple[float, float]:
        pass

    @abstractmethod
    def get_closest_node(self, lat: float, lon: float) -> int:
        pass

    @abstractmethod
    def get_node_id(self, lat: float, lon: float) -> Optional[int]:
        pass
