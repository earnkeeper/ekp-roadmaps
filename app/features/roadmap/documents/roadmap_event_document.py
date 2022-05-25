from typing import TypedDict


class RoadmapEventDocument(TypedDict):
    id: str
    updated: int
    timestamp: str
    when: str
    game: str
    milestone: str
    notes: str
    