from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from app.domain.definitions.gis import TNodeData, TNodeID

TEdge = Tuple[TNodeID, TNodeID]


class IGraph(ABC):

    @abstractmethod
    def add_node(self, id: TNodeID, node_data: Optional[TNodeData] = None):
        pass

    @abstractmethod
    def add_edge(self, node1_id: TNodeID, node2_id: TNodeID, weight: Optional[float] = None):
        pass

    @abstractmethod
    def find_shortest_path(self, node1_id: TNodeID, node2_id: TNodeID) -> List[TNodeData]:
        pass

    @abstractmethod
    def find_nearest_node(self, target_coords: Tuple[float, float]) -> TNodeID:
        pass
