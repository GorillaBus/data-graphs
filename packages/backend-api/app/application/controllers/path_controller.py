from app.application.use_cases.find_path_use_case import FindPathUseCase
from typing import Dict


class PathController:
    def __init__(self, find_path_use_case: FindPathUseCase):
        self.find_path_use_case = find_path_use_case

    def find_path(self, lat_a: float, lon_a: float, lat_b: float, lon_b: float) -> Dict[str, list]:
        result = self.find_path_use_case.execute(lat_a, lon_a, lat_b, lon_b)
        return result
