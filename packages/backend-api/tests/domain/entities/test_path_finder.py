from app.domain.ports.geo_repository import IGeoRepository
from app.domain.entities.path_finder import PathFinder
from app.infrastructure.dto.node_dto import NodeDTO


class MockGeoRepository(IGeoRepository):
    def find_ways_in_radius(self, center_coords, radius):
        # Devolver una lista de NodeDTO
        return [NodeDTO(id=1, lat=40.749817, lon=-73.985428, type='node', tags={}),
                NodeDTO(id=2, lat=40.753726, lon=-73.977229, type='node', tags={})]


def test_find_path():
    geo_repo = MockGeoRepository()
    path_finder = PathFinder(geo_repo)
    point_a = (40.748817, -73.985428)
    point_b = (40.752726, -73.977229)

    path = path_finder.find_path(point_a, point_b)

    assert isinstance(path, list)
    assert path  # Path is not empty
    assert all(isinstance(node, NodeDTO) for node in path)
