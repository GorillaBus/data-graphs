from typing import List, Tuple, Optional
from geopy.distance import geodesic
from app.infrastructure.dto.node_dto import NodeDTO
from networkx import Graph as NXGraph
from app.domain.ports.igis_graph import IGisGraph
from rtree import index


class NXGisGraph(IGisGraph):
    def __init__(self):
        self.graph = NXGraph()
        self.idx = index.Index()  # Inicializa el R-tree

    def print_graph(self):
        print("Nodes:")
        for node, data in self.graph.nodes(data=True):
            print(
                f"Node ID: {node}, Coordinates: ({data['lat']}, {data['lon']})")

        print("\nEdges:")
        for edge in self.graph.edges(data=True):
            print(f"Edge: {edge[0]} - {edge[1]}, Weight: {edge[2]['weight']}")

    def add_node(self, id: int, lat: float, lon: float):  # Removed @abstractmethod
        self.graph.add_node(id, lat=lat, lon=lon)
        # Guarda el mapeo de coordenadas a ID
        self.idx.insert(id, (lat, lon, lat, lon))

    def add_edge(self, node1_id: int, node2_id: int, weight: float):  # Removed @abstractmethod
        self.graph.add_edge(node1_id, node2_id, weight=weight)

    def get_node_coordinates(self, node_id: int) -> Tuple[float, float]:
        node_data = self.graph.nodes[node_id]
        return node_data['lat'], node_data['lon']

    def get_neighbors(self, node_id: int) -> List[Tuple[int, float]]:
        neighbors = [(neighbor, self.graph[node_id][neighbor].get('weight', 1.0))
                     for neighbor in self.graph.neighbors(node_id)]
        return neighbors

    def get_node_id(self, lat: float, lon: float) -> Optional[int]:

        print("Si que estoy llegando eh!!!", self.coord_to_id)
        # Obtiene el ID del nodo basado en las coordenadas
        return self.coord_to_id.get((lat, lon))

    def get_closest_node(self, lat: float, lon: float) -> int:
        # Busca el nodo más cercano utilizando el R-tree
        closest_items = list(self.idx.nearest((lat, lon, lat, lon), 1))
        if closest_items:
            return closest_items[0]
        return None  # o puedes lanzar una excepción si prefieres

    @classmethod
    def create_graph(cls, nodes: List[NodeDTO]) -> 'NXGisGraph':
        adapter = cls()
        for node in nodes:
            adapter.add_node(node.id, node.lat, node.lon)
        return adapter
