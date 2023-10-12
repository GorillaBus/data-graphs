from rtree import index
from multiprocessing.sharedctypes import Value
from typing import List, Tuple
import networkx as nx
from app.domain.ports.igeograph import IGeoGraph
from app.domain.definitions.gis import TNodeData, TNodeID
from app.infrastructure.adapters.nxgraph import NXGraph


class NXGeoGraph(NXGraph, IGeoGraph):
    def __init__(self):
        self.graph = nx.Graph()
        self.index = index.Index()

    def add_node(self, node_id: TNodeID, node_data: TNodeData):
        self.__index_node(node_id, node_data)
        self.graph.add_node(node_id, **node_data)

    def find_nearest_node(self, target_coords: Tuple[float, float]) -> TNodeID:
        nearest = list(self.index.nearest(
            (target_coords[1], target_coords[0], target_coords[1], target_coords[0]), 1))
        if nearest:
            return nearest[0]
        else:
            raise ValueError(
                "NXGeoGraph (find_nearest_node): could not find any graph nodes with the given coordinates")

    def __index_node(self, node_id: TNodeID, node_data: TNodeData):
        if not node_data:
            #!use domain error
            raise ValueError(
                "NXGeoGraph (index_node): node cannot be indexed with null node_data")

        lat = node_data.get('lat', None)
        lon = node_data.get('lon', None)
        if lat and lon:
            self.index.insert(node_id, (lon, lat, lon, lat))
        else:
            #!todo Time to implement a logger
            print(
                "NXGeoGraph (index_node): node {node_id} could not be indexed due to null coordinates")

    def find_shortest_path(self, node1_id: TNodeID, node2_id: TNodeID) -> List[TNodeData]:
        path = nx.shortest_path(self.graph, source=node1_id, target=node2_id)

        output = []
        for nodeId in path:
            output.append(self.graph.nodes[nodeId])

        return output
