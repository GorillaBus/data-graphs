from rtree import index
from app.domain.ports.igis_graph import IGisGraph


class GISGraph(IGisGraph):
    def __init__(self):
        super().__init__()
        self.coord_to_node_id_map = {}  # Mapa de coordenadas a IDs de nodo
        self.spatial_index = index.Index()  # Índice espacial para búsqueda eficiente

    def add_node(self, node_id, lat, lon):
        super().add_node(node_id)
        self.nodes[node_id]['coords'] = (lat, lon)
        self.coord_to_node_id_map[(lat, lon)] = node_id
        self.spatial_index.insert(node_id, (lat, lon, lat, lon))

    def get_node_id(self, lat, lon):
        return self.coord_to_node_id_map.get((lat, lon))

    def nearest_node(self, lat, lon):
        nearest = list(self.spatial_index.nearest((lat, lon, lat, lon), 1))
        return nearest[0] if nearest else None

    def nodes_within_radius(self, lat, lon, radius):
        # Implementar búsqueda de nodos dentro de un radio
        # Esto es un ejemplo simplificado y puede que necesites una implementación más compleja
        bounding_box = (lat - radius, lon - radius, lat + radius, lon + radius)
        node_ids = list(self.spatial_index.intersection(bounding_box))
        return [(node_id, self.nodes[node_id]['coords']) for node_id in node_ids]

    def get_node_coordinates(self, node_id):
        return self.nodes[node_id]['coords']
