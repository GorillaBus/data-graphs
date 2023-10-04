from app.domain.entities.path_finder import PathFinder
from typing import Dict


class FindPathUseCase:

    def __init__(self, path_finder: PathFinder):
        self.path_finder = path_finder

    def execute(self, lat_a: float, lon_a: float, lat_b: float, lon_b: float) -> Dict[str, list]:
        point_a = (lat_a, lon_a)
        point_b = (lat_b, lon_b)
        path = self.path_finder.find_path(point_a, point_b)
        return path
