from abc import ABC, abstractmethod
from typing import List, Tuple
from app.domain.definitions.gis import TGisFeature


class IGeoRepository(ABC):

    @abstractmethod
    def find_ways_in_radius(self, center_coords: Tuple[float, float], radius: float) -> List[TGisFeature]:
        pass
