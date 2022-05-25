from typing import TypedDict


class RoadmapSummaryDocument(TypedDict):
    id: str
    updated: int
    total_games: int
    total_milestones: int
    latest_milestone: str