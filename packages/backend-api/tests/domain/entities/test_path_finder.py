from app.domain.ports.geo_repository import IGeoRepository
from app.domain.entities.path_finder import PathFinder
import pytest
1


class MockGeoRepository(IGeoRepository):
    def find_ways_in_radius(self, center_coords, radius):
        return []


def test_find_path():
    geo_repo = MockGeoRepository()
    path_finder = PathFinder(geo_repo)
    point_a = (40.748817, -73.985428)
    point_b = (40.752726, -73.977229)

    path = path_finder.find_path(point_a, point_b)

    assert isinstance(path, dict)
    assert "path" in path
