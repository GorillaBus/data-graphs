from typing import List
from networkx import Graph as NXGraph
from app.infrastructure.dto.node_dto import NodeDTO


class Graph:
    def __init__(self, nodes: List[NodeDTO]):
        self._graph = NXGraph()
        self.add_nodes(nodes)

    def add_nodes(self, nodes: List[NodeDTO]):
        for node in nodes:
            self._graph.add_node(node.id, lat=node.lat, lon=node.lon)

    @property
    def graph(self) -> NXGraph:
        return self._graph

    @staticmethod
    def create_graph(node_dtos: List[NodeDTO]) -> 'Graph':
        graph = Graph()
        # Add nodes to the graph
        for node_dto in node_dtos:
            graph.add_node(node_dto.id, lat=node_dto.lat, lon=node_dto.lon)

        # Assumes each NodeDTO has a list of neighbours in the form of IDs
        for node_dto in node_dtos:
            for neighbor_id in node_dto.tags.get('neighbors', []):
                # Asumiendo que la distancia es 1, modificar según sea necesario
                graph.add_edge(node_dto.id, neighbor_id)

        return graph  # Devolver el grafo
