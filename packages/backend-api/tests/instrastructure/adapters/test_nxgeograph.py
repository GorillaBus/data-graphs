import unittest
from app.infrastructure.adapters.nxgeograph import NXGeoGraph


class TestNXGraph(unittest.TestCase):

    def setup_method(self, method):
        self.mock_nodes = [
            {"name": "Node1", "lat": 51.0, "lon": 11.0},
            {"name": "Node2", "lat": 52.0, "lon": 12.0},
            {"name": "Node3", "lat": 53.0, "lon": 13.0}
        ]

    def test_add_node(self):
        graph = NXGeoGraph()
        node_data = self.mock_nodes[0]
        graph.add_node(1, node_data)

        # Graph exists
        self.assertIn(1, graph.graph.nodes)

        # Graph has attributes
        node_attributes = graph.graph.nodes[1]

        self.assertEqual(node_attributes['name'], self.mock_nodes[0]['name'])
        self.assertEqual(node_attributes['lat'], self.mock_nodes[0]['lat'])
        self.assertEqual(node_attributes['lon'], self.mock_nodes[0]['lon'])

    def test_add_edge(self):
        graph = NXGeoGraph()

        graph.add_node(1, self.mock_nodes[0])
        graph.add_node(2, self.mock_nodes[1])
        graph.add_edge(1, 2, weight=5.0)

        # Nodes are neighbors
        self.assertIn(2, graph.graph[1])

    def test_find_shortest_path(self):
        graph = NXGeoGraph()
        graph.add_node(1, self.mock_nodes[0])
        graph.add_node(2, self.mock_nodes[1])
        graph.add_node(3, self.mock_nodes[2])

        edges = [
            (1, 2, 1.0),
            (2, 3, 1.0),
        ]
        for edge in edges:
            graph.add_edge(edge[0], edge[1], edge[2])

        expected_path = [
            self.mock_nodes[0],
            self.mock_nodes[1],
            self.mock_nodes[2]
        ]

        path = graph.find_shortest_path(1, 3)
        print(">>>>>>>> PATH", path)
        self.assertEqual(path, expected_path)


if __name__ == '__main__':
    unittest.main()
