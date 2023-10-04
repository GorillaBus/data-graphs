import requests
from app.domain.ports.geo_repository import IGeoRepository

from app.infrastructure.dto.node_dto import NodeDTO
from typing import List, Tuple


class OverPassGeoRepository(IGeoRepository):

    def find_ways_in_radius(self, center_coords: Tuple[float, float], radius: float) -> List[NodeDTO]:
        overpass_url = "https://overpass-api.de/api/interpreter"
        overpass_query = f"""
        [out:json];
        (way["highway"](around:{radius},{center_coords[0]},{center_coords[1]}););
        (._;>;);
        out body;
        """.strip()

        try:
            response = requests.get(overpass_url, params={
                                    'data': overpass_query})
            response.raise_for_status()
            response_data = response.json()

            # Ensure we found 'elements' on the response
            if 'elements' not in response_data:
                print(
                    'overpass: response has no elements field (unexpected response)')
                return None

            # Create DTOs from response
            node_dto_list = [NodeDTO(
                type=element['type'],
                id=element['id'],
                lat=element['lat'],
                lon=element['lon'],
                tags=element.get('tags', None)
            )
                for element in response_data['elements']
                if element['type'] == 'node']  # Ensure the element is a node

            return node_dto_list

        except requests.HTTPError:
            print(
                f"overpass: error HTTP {response.status_code} al realizar la consulta: {response.text}")
        except ValueError:
            print("overpass: error decoding response.")
        return None
