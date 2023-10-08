from abc import ABC, abstractmethod
from typing import List, Tuple
from app.infrastructure.dto.node_dto import NodeDTO


class IPathFinder(ABC):

    @abstractmethod
    def find_path(self, graph, point_a: Tuple[float, float], point_b: Tuple[float, float]) -> List[NodeDTO]:
        pass
