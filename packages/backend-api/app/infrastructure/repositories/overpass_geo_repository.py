import requests
from typing import Any, Dict, List, Tuple
from app.domain.ports.geo_repository import IGeoRepository
from app.infrastructure.dto.way_dto import WayDTO


class OverPassGeoRepository(IGeoRepository):

    def find_ways_in_radius(self, center_coords: Tuple[float, float], radius: float) -> List[WayDTO]:
        overpass_url = "https://overpass-api.de/api/interpreter"
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
            response = requests.get(overpass_url, params={
                                    'data': overpass_query})
            response.raise_for_status()
            response_data = response.json()

            # Asegúrate de que encontraste 'elements' en la respuesta
            if 'elements' not in response_data:
                print(
                    'overpass: la respuesta no tiene el campo elements (respuesta inesperada)')
                return []

            return self.__process_overpass_response__(response_data)

        except requests.HTTPError:
            print(
                f"overpass: error HTTP {response.status_code if response else 'unknown'} al realizar la consulta: {response.text if response else 'unknown'}")
        except ValueError:
            print("overpass: error al decodificar la respuesta.")
        return []

    def __process_overpass_response__(self, response: Dict[str, Any]) -> List[WayDTO]:
        ways = []
        nodes_cache = {}  # Un diccionario para almacenar los detalles de los nodos por ID

        # Primero, procesa todos los nodos
        for element in response['elements']:
            if element['type'] == 'node':
                nodes_cache[element['id']] = {
                    "lat": element['lat'], "lon": element['lon']}

        # Luego, procesa los caminos (ways)
        for element in response['elements']:
            if element['type'] == 'way':
                nodes = [nodes_cache[node_id]
                         for node_id in element['nodes'] if node_id in nodes_cache]
                way = WayDTO(
                    id=element['id'],
                    nodes=nodes,
                    tags=element.get('tags')
                )
                ways.append(way)

        return ways
