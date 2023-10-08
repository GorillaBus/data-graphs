from dataclasses import dataclass, asdict
from typing import Dict, Any, List


@dataclass
class WayDTO:
    id: int
    nodes: List[Dict[str, float]]
    tags: Dict[str, Any]

    def to_dict(self):
        return asdict(self)
