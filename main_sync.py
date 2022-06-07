
import asyncio
import logging

from decouple import AutoConfig
from ekp_sdk import BaseContainer

from db.roadmap_event_repo import RoadmapEventRepo
from sync.roadmap_sync_service import RoadmapSyncService


class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig('.env')

        super().__init__(config)

        SHEET_ID=config("SHEET_ID")
        
        # DB

        self.roadmap_event_repo = RoadmapEventRepo(
            mg_client=self.mg_client,
        )

        # Services
        
        self.roadmap_sync_service = RoadmapSyncService(
            roadmap_event_repo=self.roadmap_event_repo,
            google_sheets_client=self.google_sheets_client,
            sheet_id=SHEET_ID
        )
        
if __name__ == '__main__':
    container = AppContainer()

    logging.basicConfig(level=logging.INFO)

    logging.info("🚀 Application Start")

    loop = asyncio.get_event_loop()

    loop.run_until_complete(
        container.roadmap_sync_service.sync_roadmap_events()
    )
