import os

from apiclient import discovery
from google.oauth2 import service_account
from ekp_sdk.services import CacheService
from datetime import datetime

from app.features.roadmap.documents.roadmap_event_document import RoadmapEventDocument


class RoadmapService:

    def __init__(
        self,
        cache_service: CacheService,
        spreadsheet_id: str
    ):
        self.cache_service = cache_service
        self.spreadsheet_id = spreadsheet_id

        scopes = ["https://www.googleapis.com/auth/drive",
                  "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
        secret_file = os.path.join(os.getcwd(), 'secret/credentials.json')
        credentials = service_account.Credentials.from_service_account_file(
            secret_file, scopes=scopes)
        self.service = discovery.build('sheets', 'v4', credentials=credentials)

    async def get_documents(self):
        roadmap_event_values = await self.cache_service.wrap(
            "roadmap_event_values",
            lambda: self.get_roadmap_event_values(),
            ex=120
        )
        
        now = datetime.now().timestamp()
        
        documents = []
        
        for event in roadmap_event_values:
            if len(event) <= 5:
                continue
             
            month = event[0]
            qtr = event[1]
            year = event[2]
            game = event[3]
            milestone = event[4]
            notes = event[5]
            when = None
            timestamp = None
            if not year:
                continue
            
            year = int(year)
            
            if not qtr:
                continue
            
            qtr = int(qtr)
            
            if qtr:
                when = f"Q{qtr} {year}"
                month = qtr * 3
                timestamp = datetime(year,month,1).timestamp()
            
            id = f"{game}_{milestone}_{timestamp}"
            
            document: RoadmapEventDocument = {
                'game': game,
                'milestone': milestone,
                'notes': notes,
                'timestamp': timestamp,
                'updated': now,
                'when': when,
                'id': id
            }
            
            documents.append(document)
        return documents

    async def get_roadmap_event_values(self):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=self.spreadsheet_id,
            range='Roadmaps!A2:F'
        ).execute()

        return result.get('values', [])
