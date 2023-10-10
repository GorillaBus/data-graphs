import requests
from typing import Any, Dict, List, Tuple
from app.domain.ports.geo_repository import IGeoRepository
from app.domain.definitions.gis import TGisFeature

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


class OverPassGeoRepository(IGeoRepository):

    def find_ways_in_radius(self, center_coords: Tuple[float, float], radius: float) -> List[TGisFeature]:

        overpass_query = f"""
        [out:json];
        (
            way["highway"](around:{radius},{center_coords[0]},{center_coords[1]});
            node(around:{radius},{center_coords[0]},{center_coords[1]});
        );
        (._;>;);
        out body;
        """.strip()

        try:
            response = requests.get(OVERPASS_URL, params={
                                    'data': overpass_query})
            response.raise_for_status()
            response_data = response.json()

            # We are expecting 'elements'
            if 'elements' not in response_data:
                raise ValueError(
                    'overpass: la respuesta no tiene el campo elements (respuesta inesperada)')  # Usar damain error

            return self.__process_overpass_response__(response_data)

        except requests.HTTPError as e:
            print(
                f"overpass: error HTTP {e.response.status_code if e.response else 'unknown'} al realizar la consulta: {e.response.text if e.response else 'unknown'}")  # Usar damain error
        except ValueError as ve:
            # Usar damain error
            print(f"overpass: error al decodificar la respuesta: {ve}")
        return []

    def __process_overpass_response__(self, response: Dict[str, Any]) -> List[TGisFeature]:
        features = []
        nodes_cache = {}

        # nodes
        for element in response['elements']:
            if element['type'] == 'node':
                nodes_cache[element['id']] = {
                    "id": element['id'],
                    "lat": element['lat'],
                    "lon": element['lon']
                }

        # features
        for element in response['elements']:
            if element['type'] == 'way':
                nodes = [nodes_cache.get(node_id, {})
                         for node_id in element['nodes']]

                way: TGisFeature = {
                    "id": element['id'],
                    "nodes": nodes,
                    "tags": element.get('tags', {})
                }
                features.append(way)

        return features
