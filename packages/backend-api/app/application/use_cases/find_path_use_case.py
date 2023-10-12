from app.domain.ports.igraph import IGraph
from app.domain.ports.geo_repository import IGeoRepository
from app.domain.entities.geo_path_finder import GeoPathFinder
from app.domain.errors.error import Error
from typing import Type, Dict


class FindPathUseCase:

    def __init__(self, geo_repository: IGeoRepository, graph_class: Type[IGraph]):
        self.geo_path_finder = GeoPathFinder(geo_repository, graph_class)

    def execute(self, lat_a: float, lon_a: float, lat_b: float, lon_b: float) -> Dict[str, list]:
        try:
            point_a = (lat_a, lon_a)
            point_b = (lat_b, lon_b)
            found_path = self.geo_path_finder.find_path(point_a, point_b)

            return found_path
        except Error as e:
            raise
