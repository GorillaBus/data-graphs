from app.domain.entities.geo_path_finder import GeoPathFinder
from app.domain.errors.error import Error
from typing import Dict


class FindPathUseCase:

    def __init__(self, geo_path_finder: GeoPathFinder):
        self.geo_path_finder = geo_path_finder

    def execute(self, lat_a: float, lon_a: float, lat_b: float, lon_b: float) -> Dict[str, list]:
        try:
            point_a = (lat_a, lon_a)
            point_b = (lat_b, lon_b)
            path = self.geo_path_finder.find_path(point_a, point_b)
            return path
        except Error as e:
            raise
