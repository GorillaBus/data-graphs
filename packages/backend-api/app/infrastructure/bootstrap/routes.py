from flask import Blueprint, request, jsonify
from .dependencies import build_path_controller

bp = Blueprint('routes', __name__)
path_controller = build_path_controller()


@bp.route('/api/path/<float:lat_a>/<float:lon_a>/<float:lat_b>/<float:lon_b>', methods=['GET'])
def find_path(lat_a, lon_a, lat_b, lon_b):
    result = path_controller.find_path(lat_a, lon_a, lat_b, lon_b)
    return jsonify(result)
