from geopy.distance import geodesic
from typing import Tuple, List
from app.domain.errors.error import Error
from app.domain.ports.geo_repository import IGeoRepository
from app.domain.ports.igis_graph import IGisGraph
from app.domain.ports.ipath_finder import IPathFinder
from app.infrastructure.dto.node_dto import NodeDTO


MAX_DISTANCE = 1200


class GeoPathFinder:
    def __init__(self, geo_repo: IGeoRepository, path_finder: IPathFinder, graph_class: IGisGraph):
        self.geo_repo = geo_repo
        self.path_finder = path_finder
        self.graph_class = graph_class

    def find_path(self, point_a: Tuple[float, float], point_b: Tuple[float, float]) -> List[NodeDTO]:
        # A-B distance
        distance = geodesic(point_a, point_b).meters
        if distance > MAX_DISTANCE:
            raise Error('INVALID_DISTANCE')

        # Calcular el punto medio entre A y B
        midpoint = ((point_a[0] + point_b[0]) / 2,
                    (point_a[1] + point_b[1]) / 2)

        # Calcular el radio del buffer
        buffer_radius = distance * 2

        # Get features
        nodes = self.geo_repo.find_ways_in_radius(
            midpoint, buffer_radius/2)
        return nodes
        # Create graph
        featured_graph = self.graph_class.create_graph(nodes)

        # Convertir coordenadas a IDs de nodo
        start_node_id = featured_graph.get_closest_node(*point_a)
        end_node_id = featured_graph.get_closest_node(*point_b)

        # Find and return the path

        return self.path_finder.find_path(featured_graph, start_node_id, end_node_id)
