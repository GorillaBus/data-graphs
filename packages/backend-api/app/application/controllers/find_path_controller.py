from flask import request, jsonify, abort  # !decouple Flask
from app.application.use_cases.find_path_use_case import FindPathUseCase
from app.domain.entities.path_finder import PathFinder
from app.infrastructure.repositories.overpass_geo_repository import OverPassGeoRepository

# Dependencies
geo_repo = OverPassGeoRepository()
path_finder = PathFinder(geo_repo)
find_path_use_case = FindPathUseCase(path_finder)


class FindPathController:
    @staticmethod
    def handle_request(lat_a: float, lon_a: float, lat_b: float, lon_b: float):
        # Run use-case
        path_dto_list = find_path_use_case.execute(lat_a, lon_a, lat_b, lon_b)

        # Map DTO to response
        path_json = [dto.to_dict() for dto in path_dto_list]

        response = {
            "path": path_json
        }
        return jsonify(response)
