import unittest
from app.infrastructure.adapters.nxgraph import NXGraph


class TestNXGraph(unittest.TestCase):

    def test_add_node(self):
        graph = NXGraph()
        node_data = {"name": "Node1", "lat": 50.0, "lon": 10.0}
        graph.add_node(1, node_data)

        # Graph exists
        self.assertIn(1, graph.graph.nodes)

        # Graph has attributes
        node_attributes = graph.graph.nodes[1]

        self.assertEqual(node_attributes['name'], "Node1")
        self.assertEqual(node_attributes['lat'], 50.0)
        self.assertEqual(node_attributes['lon'], 10.0)

    def test_add_edge(self):
        graph = NXGraph()
        graph.add_node(1)
        graph.add_node(2)
        graph.add_edge(1, 2, weight=5.0)

        # Nodes are neighbors
        self.assertIn(2, graph.graph[1])

    def test_find_shortest_path(self):
        graph = NXGraph()
        nodes = [1, 2, 3]
        edges = [
            (1, 2, 1.0),
            (2, 3, 1.0)
        ]
        for node in nodes:
            graph.add_node(node, node_data={"some": "key"})

        for edge in edges:
            graph.add_edge(edge[0], edge[1], edge[2])

        expected_path = {
            1: {"some": "key"},
            2: {"some": "key"},
            3: {"some": "key"}
        }

        path = graph.find_shortest_path(1, 3)

        self.assertEqual(path, expected_path)


if __name__ == '__main__':
    unittest.main()
