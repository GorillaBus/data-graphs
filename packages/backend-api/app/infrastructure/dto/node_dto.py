from dataclasses import dataclass, asdict
from typing import Dict, List, Union, Optional


@dataclass
class NodeDTO:
    id: int
    type: str
    lat: float
    lon: float
    tags: Optional[Dict[str, Union[str, int, float]]] = None
    nodes: Optional[List['NodeDTO']] = None

    def to_dict(self) -> dict:
        return asdict(self)
