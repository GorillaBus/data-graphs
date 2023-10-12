from flask import jsonify, make_response
from app.domain.errors.error import Error
from app.application.use_cases.find_path_use_case import FindPathUseCase
from app.infrastructure.repositories.overpass_geo_repository import OverPassGeoRepository
from app.infrastructure.adapters.nxgeograph import NXGeoGraph

# Dependencies
geo_repo = OverPassGeoRepository()
graph_class = NXGeoGraph
find_path_use_case = FindPathUseCase(geo_repo, graph_class)


class FindPathController:
    @staticmethod
    def handle_request(lat_a: float, lon_a: float, lat_b: float, lon_b: float):
        try:
            # Run use-case
            found_path_way = find_path_use_case.execute(
                lat_a, lon_a, lat_b, lon_b)

            response = {
                "path": found_path_way
            }
            return jsonify(response)

        except Error as e:

            api_error_message = "An unknown error occurred"

            if e.error_code == 4002:
                api_error_message = "Whoa, that's a long journey, man! The cosmic law of MAX_DISTANCE has been breached."
            else:
                api_error_message = e.description

            error_response = {
                "error": api_error_message
            }

            print(e)
            return make_response(jsonify(error_response), 400)
