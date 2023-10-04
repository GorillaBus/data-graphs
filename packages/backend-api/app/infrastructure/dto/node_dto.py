from dataclasses import dataclass, asdict
from typing import Optional, Dict, Union


@dataclass
class NodeDTO:
    type: str
    id: int
    lat: float
    lon: float
    tags: Optional[Dict[str, Union[str, int, float]]] = None

    def to_dict(self) -> dict:
        return asdict(self)
