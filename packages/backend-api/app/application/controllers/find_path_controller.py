from flask import jsonify, make_response
from app.domain.errors.error import Error
from app.domain.entities.geo_path_finder import GeoPathFinder
from app.application.use_cases.find_path_use_case import FindPathUseCase
from app.infrastructure.repositories.overpass_geo_repository import OverPassGeoRepository
from app.infrastructure.adapters.algos.astar_path_finder import AStarPathFinder
from app.infrastructure.adapters.nx_gis_graph import NXGisGraph

# Dependencies
path_finder_algo = AStarPathFinder()
geo_repo = OverPassGeoRepository()
path_finder = GeoPathFinder(geo_repo, path_finder_algo, NXGisGraph)
find_path_use_case = FindPathUseCase(path_finder)


class FindPathController:
    @staticmethod
    def handle_request(lat_a: float, lon_a: float, lat_b: float, lon_b: float):
        try:
            # Run use-case
            path_dto_list = find_path_use_case.execute(
                lat_a, lon_a, lat_b, lon_b)

            # Map DTO to response
            path_json = [dto.to_dict() for dto in path_dto_list]

            response = {
                "path": path_json
            }
            return jsonify(response)

        except Error as e:

            api_error_message = "An unknown error occurred"

            if e.error_code == 4002:
                api_error_message = "Whoa, that's a long journey, man! The cosmic law of MAX_DISTANCE has been breached."

            error_response = {
                "error": api_error_message
            }

            print(e)
            return make_response(jsonify(error_response), 400)
