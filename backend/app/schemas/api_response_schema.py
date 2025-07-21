from typing import Any, Optional
from dataclasses import dataclass, asdict
from flask import Response, jsonify

@dataclass
class APIResponseSchema:
    success: bool
    message: str
    code: int
    data: Optional[Any] = None

    def to_dict(self):
        return asdict(self)

    def to_json(self) -> Response:
        return jsonify(self.to_dict()), self.code