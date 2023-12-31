from typing import List
from dataclasses import dataclass, asdict
from typing import Dict, List, Union, Optional, Any

TNodeData = Dict[str, Any]
TNodeID = int


@dataclass
class TGisNode():
    id: int
    type: str
    lat: float
    lon: float
    tags: Optional[Dict[str, Union[str, int, float]]] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TGisFeature():
    id: int
    nodes: List[TGisNode]
    tags: Dict[str, Any]

    def to_dict(self) -> dict:
        return asdict(self)
