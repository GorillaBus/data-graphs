from app.domain.ports.geo_repository import IGeoRepository

from typing import List, Tuple


class OverPassGeoRepository(IGeoRepository):

    def find_ways_in_radius(self, center_coords: Tuple[float, float], radius: float) -> List[dict]:
        # Implementa la lógica para interactuar con la API de OSM Over Pass
        pass
