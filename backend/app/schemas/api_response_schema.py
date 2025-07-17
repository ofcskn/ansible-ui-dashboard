from typing import Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class APIResponseSchema:
    success: bool
    message: str
    code: int
    data: Optional[Any] = None

    def to_dict(self):
        return asdict(self)