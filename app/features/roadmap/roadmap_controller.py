from ekp_sdk.services import ClientService
from ekp_sdk.util import client_currency, client_path
from app.features.roadmap.roadmap_page import roadmap_page

from app.features.roadmap.services.roadmap_service import RoadmapService

ROADMAP_EVENTS_COLLECTION_NAME = "roadmap_events_collection"

class RoadmapController:
    def __init__(
        self,
        client_service: ClientService,
        roadmap_service: RoadmapService,
    ):
        self.client_service = client_service
        self.roadmap_service = roadmap_service
        self.path = 'roadmaps'

    async def on_connect(self, sid):
        await self.client_service.emit_menu(
            sid,
            'calendar',
            'Roadmaps',
            self.path
        )
        await self.client_service.emit_page(
            sid,
            self.path,
            roadmap_page(ROADMAP_EVENTS_COLLECTION_NAME)
        )

    async def on_client_state_changed(self, sid, event):

        path = client_path(event)

        if (path != self.path):
            return

        await self.client_service.emit_busy(sid, ROADMAP_EVENTS_COLLECTION_NAME)

        documents = await self.roadmap_service.get_documents()

        await self.client_service.emit_documents(
            sid,
            ROADMAP_EVENTS_COLLECTION_NAME,
            documents
        )

        await self.client_service.emit_done(sid, ROADMAP_EVENTS_COLLECTION_NAME)
