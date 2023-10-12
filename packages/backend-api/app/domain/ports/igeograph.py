from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from app.domain.definitions.gis import TNodeID


class IGeoGraph(ABC):

    @abstractmethod
    def find_nearest_node(self, target_coords: Tuple[float, float]) -> TNodeID:
        pass
