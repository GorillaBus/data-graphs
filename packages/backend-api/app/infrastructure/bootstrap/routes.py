from flask import Blueprint, request
from app.application.controllers.find_path_controller import FindPathController

bp = Blueprint('routes', __name__)


@bp.route('/api/find-path/<float:lat_a>/<float:lon_a>/<float:lat_b>/<float:lon_b>', methods=['GET'])
def find_path_route(lat_a, lon_a, lat_b, lon_b):
    return FindPathController.handle_request(lat_a, lon_a, lat_b, lon_b)
