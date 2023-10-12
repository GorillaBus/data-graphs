import time
from geopy.distance import geodesic
from typing import Type, Tuple, List, Any, Dict
from app.domain.errors.error import Error
from app.domain.ports.igraph import IGraph
from app.domain.ports.geo_repository import IGeoRepository
from app.domain.definitions.gis import TGisFeature, TNodeID

MAX_DISTANCE = 2000


def profile_method(method):
    def timed(*args, **kw):
        start_time = time.time()
        result = method(*args, **kw)
        end_time = time.time()

        print(
            f"{method.__name__} - Tiempo de ejecución: {end_time - start_time:.4f} segundos")
        return result

    return timed


class GeoPathFinder:
    def __init__(self, geo_repo: IGeoRepository, graph_class: Type[IGraph]):
        self.geo_repo = geo_repo
        self.graph_class = graph_class

    def find_path(self, point_a: Tuple[float, float], point_b: Tuple[float, float]) -> TGisFeature:
        # A-B distance
        distance = geodesic(point_a, point_b).meters
        if distance > MAX_DISTANCE:
            raise Error('INVALID_DISTANCE')

        midpoint = ((point_a[0] + point_b[0]) / 2,
                    (point_a[1] + point_b[1]) / 2)

        buffer_radius = distance * 2
        found_paths = self.geo_repo.find_ways_in_radius(
            midpoint, buffer_radius)

        graph = self.__create_graph_from_paths(found_paths)

        # find nearest nodes to the given pints (coords)
        nearest_node_a = graph.find_nearest_node(point_a)
        nearest_node_b = graph.find_nearest_node(point_b)
        shortest_path = graph.find_shortest_path(
            nearest_node_a, nearest_node_b)

        return shortest_path

    def __create_graph_from_paths(self, features: List[Dict[str, Any]]) -> IGraph:
        graph = self.graph_class()

        for feature_dict in features:
            nodes_list = feature_dict.get('nodes', [])
            for node_dict in nodes_list:
                node_id = node_dict.get('id')
                graph.add_node(node_id, node_dict)

            for i in range(len(nodes_list) - 1):
                node1_id = nodes_list[i]['id']
                node2_id = nodes_list[i + 1]['id']
                graph.add_edge(node1_id, node2_id)
        return graph

    def __find_nearest_node_in_graph(self, graph: IGraph, target_coords: Tuple[float, float]) -> TNodeID:
        min_distance = float("inf")
        nearest_node_id = None

        for node_id, attributes in graph.graph.nodes(data=True):
            node_lat = attributes.get('lat')
            node_lon = attributes.get('lon')
            if node_lat is None or node_lon is None:
                continue

            node_coords = (node_lat, node_lon)

            distance = geodesic(target_coords, node_coords).meters

            if distance < min_distance:
                min_distance = distance
                nearest_node_id = node_id

        if nearest_node_id is None:
            #!trhow domain error
            raise ValueError(
                "No se pudo encontrar un nodo cercano a las coordenadas proporcionadas.")

        return nearest_node_id


# Aplicar el decorador a todos los métodos de la clase
for method_name, method in vars(GeoPathFinder).items():
    if callable(method):
        setattr(GeoPathFinder, method_name, profile_method(method))
