from app.utils.page_title import page_title
from ekp_sdk.ui.components import Container, Datatable, documents, Column, Span, Paragraphs, Div, is_busy, collection, Row, Col, Link, Div


def roadmap_page(ROADMAP_EVENTS_COLLECTION_NAME):
    return Container([
        page_title('calendar', 'Roadmap Events'),
        Paragraphs([
            "We search the space for game roadmaps so that you don't have to.",
                   "Which games have roadmap events coming up? The list below shows the soonest first.",
                   "Looking for a certain game? Search for it's name below."
                   ]),
        Div([], "mb-3"),
        table_row(ROADMAP_EVENTS_COLLECTION_NAME)
    ])


def table_row(ROADMAP_EVENTS_COLLECTION_NAME):
    return Datatable(
        data=documents(ROADMAP_EVENTS_COLLECTION_NAME),
        default_sort_field_id="timestamp",
        search_hint="Search by game, milestones, or notes content..",
        pagination_per_page=50,
        busy_when=is_busy(collection(ROADMAP_EVENTS_COLLECTION_NAME)),
        columns=[
            Column(
                id="timestamp",
                format="$.when",
                title="When",
                sortable=True,
                width="100px"
            ),
            Column(
                id="game",
                sortable=True,
                searchable=True,
                width="160px",
                cell=game_cell()
            ),
            Column(
                id="milestone",
                searchable=True,
                width="340px"
            ),
            Column(
                id="notes",
                searchable=True,
                cell=Span("$.notes"),
                min_width="400px"
            ),
        ]
    )

def game_cell():
    return Div([
        Link(
            when="$.game_link",
            href="$.game_link",
            content="$.game",
            external=True,
            external_icon=True
        ),
        Span("$.game", when={ "not": "$.game_link" })
    ])
