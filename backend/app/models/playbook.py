from dataclasses import dataclass, asdict

@dataclass
class PlaybookModel:
    id: int
    name: str
    description: str

    def to_dict(self):
        return asdict(self)