from decouple import AutoConfig
from ekp_sdk import BaseContainer
from app.features.roadmap.roadmap_controller import RoadmapController

from app.features.roadmap.services.roadmap_service import RoadmapService


class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig(".env")

        super().__init__(config)

        SPREADSHEET_ID=config("SPREADSHEET_ID")

        # FEATURES - Roadmap

        self.roadmap_service = RoadmapService(
            cache_service=self.cache_service,
            spreadsheet_id=SPREADSHEET_ID
        )

        self.roadmap_controller = RoadmapController(
            client_service=self.client_service,
            roadmap_service = self.roadmap_service
        )


if __name__ == '__main__':
    container = AppContainer()

    container.client_service.add_controller(container.roadmap_controller)

    container.client_service.listen()
