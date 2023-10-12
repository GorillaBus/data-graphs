from typing import List, Tuple, Optional
import networkx as nx
from app.domain.ports.igraph import IGraph
from app.domain.definitions.gis import TNodeData, TNodeID


class NXGraph(IGraph):
    def __init__(self):
        self.graph = nx.Graph()

    def add_node(self, node_id: TNodeID, node_data: Optional[TNodeData] = None):

        if node_data is not None:
            self.graph.add_node(node_id, **node_data)
        else:
            self.graph.add_node(node_id)

    def add_edge(self, node1_id: TNodeID, node2_id: TNodeID, weight: Optional[float] = None):
        if weight is not None:
            self.graph.add_edge(node1_id, node2_id, weight=weight)
        else:
            self.graph.add_edge(node1_id, node2_id)

    def find_shortest_path(self, node1_id: TNodeID, node2_id: TNodeID) -> List[TNodeData]:
        shortest_path_ids = nx.shortest_path(
            self.graph, source=node1_id, target=node2_id)

        path_nodes = {}
        for nodeId in shortest_path_ids:
            path_nodes[nodeId] = self.graph.nodes[nodeId]

        return path_nodes
