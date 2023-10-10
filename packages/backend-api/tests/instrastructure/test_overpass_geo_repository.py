import unittest
from unittest.mock import patch, Mock
from app.infrastructure.repositories.overpass_geo_repository import OverPassGeoRepository


class TestOverPassGeoRepository(unittest.TestCase):

    @patch('app.infrastructure.repositories.overpass_geo_repository.requests.get')
    def test_find_ways_in_radius(self, mock_get):

        # Mocked data
        mock_response = Mock()
        mock_response.json.return_value = {
            'elements': [
                {
                    'type': 'node',
                    'id': 1234,
                    'lat': 50.0,
                    'lon': 10.0
                },
                {
                    'type': 'way',
                    'id': 5678,
                    'nodes': [1234],
                    'tags': {'highway': 'primary'}
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Test
        repo = OverPassGeoRepository()
        result = repo.find_ways_in_radius((50.0, 10.0), 1000)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], 5678)
        self.assertEqual(result[0]['nodes'][0]['id'], 1234)
        self.assertEqual(result[0]['tags']['highway'], 'primary')


if __name__ == '__main__':
    unittest.main()
