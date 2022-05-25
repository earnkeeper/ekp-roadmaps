from typing import TypedDict


class RoadmapEventDocument(TypedDict):
    game: str
    game_link: str
    id: str
    milestone: str
    month_str: str
    notes: str
    timestamp: str
    updated: int
    when: str