from app.utils.page_title import page_title
from ekp_sdk.ui.components import Container, Datatable, documents, Column, Span


def roadmap_page(ROADMAP_EVENTS_COLLECTION_NAME):
    return Container([
        page_title('calendar', 'Roadmap Events'),
        table_row(ROADMAP_EVENTS_COLLECTION_NAME)
    ])


def table_row(ROADMAP_EVENTS_COLLECTION_NAME):
    return Datatable(
        data=documents(ROADMAP_EVENTS_COLLECTION_NAME),
        columns=[
            Column(
                id="timestamp",
                format="$.when",
                sortable=True,
                width="100px"
            ),
            Column(
                id="game",
                sortable=True,
                searchable=True,
                width="160px"
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
