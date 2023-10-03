from app.domain.ports.geo_repository import IGeoRepository
from geopy.distance import geodesic
from shapely.geometry import Point
from shapely.ops import unary_union
from typing import Tuple, Dict, List


MAX_DISTANCE = 1000


class PathFinder:
    def __init__(self, geo_repo: IGeoRepository):
        self.geo_repo = geo_repo

    def find_path(self, point_a: Tuple[float, float], point_b: Tuple[float, float]) -> Dict[str, List[Tuple[float, float]]]:
        # A-B distance
        distance = geodesic(point_a, point_b).meters
        if distance > MAX_DISTANCE:
            raise ValueError(
                f"Whoa, that's a long journey, man! The cosmic law of MAX_DISTANCE has been breached.")

        # Create buffer
        point_a_geom, point_b_geom = Point(point_a), Point(point_b)
        buffer_radius = distance * 2
        buffer_a, buffer_b = point_a_geom.buffer(
            buffer_radius), point_b_geom.buffer(buffer_radius)
        united_buffer = unary_union([buffer_a, buffer_b])

        # Find center
        buffer_centroid = united_buffer.centroid.coords[0]

        # Get features
        features = self.geo_repo.find_ways_in_radius(
            buffer_centroid, buffer_radius)

        return {
            "path": []
        }
