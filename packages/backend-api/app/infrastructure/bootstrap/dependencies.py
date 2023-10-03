from app.domain.entities.path_finder import PathFinder
from app.infrastructure.repositories.overpass_geo_repository import OverPassGeoRepository
from app.application.use_cases.find_path_use_case import FindPathUseCase
from app.application.controllers.path_controller import PathController


def build_path_controller() -> PathController:
    geo_repo = OverPassGeoRepository()
    path_finder = PathFinder(geo_repo)
    find_path_use_case = FindPathUseCase(path_finder)
    path_controller = PathController(find_path_use_case)
    return path_controller
