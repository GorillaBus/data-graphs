import unittest
from app.infrastructure.adapters.nxgraph import NXGraph


class TestNXGraph(unittest.TestCase):

    def setup_method(self, method):
        self.mock_nodes = [1, 2, 3]

    def test_add_node(self):
        graph = NXGraph()
        graph.add_node(1)

        # Graph exists
        self.assertIn(1, graph.graph.nodes)

    def test_add_edge(self):
        graph = NXGraph()

        graph.add_node(1)
        graph.add_node(2)
        graph.add_edge(1, 2, 1.0)

        # Nodes are neighbors
        self.assertIn(2, graph.graph[1])

    def test_find_shortest_path(self):
        graph = NXGraph()
        nodes = self.mock_nodes
        edges = [
            (1, 2, 1.0),
            (2, 3, 1.0)
        ]

        graph.add_node(nodes[0])
        graph.add_node(nodes[1])
        graph.add_node(nodes[2])

        for edge in edges:
            graph.add_edge(edge[0], edge[1], edge[2])

        expected_path = self.mock_nodes
        path = graph.find_shortest_path(1, 3)

        self.assertEqual(path, expected_path)


if __name__ == '__main__':
    unittest.main()
