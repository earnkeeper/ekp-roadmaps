import logging
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
        roadmap_event_values = await self.get_roadmap_event_values()
        game_links = await self.get_game_roadmap_links()
        game_links_map = {}
        for game_link in game_links:
            if len(game_link) < 2:
                continue
            
            game_links_map[game_link[0]] = game_link[1]
        
        print(game_links_map)
        
        now = datetime.now().timestamp()
        
        documents = []
        
        for event in roadmap_event_values:
            if len(event) < 5:
                continue
             
            month = event[0]
            qtr = event[1]
            year = event[2]
            game = event[3]
            milestone = event[4]
            notes = ""
            timestamp = None
            month_str = None

            if not year:
                logging.warn(f"Skipping milestone for {game} due to missing year")
                continue
            
            year = int(year)

            if (len(event) > 5):
                notes = event[5]
            
            if month and not qtr:
                month = int(month)
                qtr = int((month / 3)) + 1
                timestamp = datetime(year,month,1)
                month_str = timestamp.strftime('%b %Y')
                timestamp = timestamp.timestamp()
            
            if not qtr:
                logging.warn(f"Skipping milestone for {game} due to missing quarter")
                continue
            
            qtr = int(qtr)
            

            when = f"Q{qtr} {year}"
            month = qtr * 3
            if not timestamp:
                timestamp = datetime(year,month,1).timestamp()
            
            id = f"{game}_{milestone}_{timestamp}"
            

            game_link = None
            
            if game in game_links_map:            
                game_link = game_links_map[game]
            
            document: RoadmapEventDocument = {
                'game': game,
                'game_link': game_link,
                'id': id,
                'milestone': milestone,
                'month_str': month_str,
                'notes': notes,
                'timestamp': timestamp,
                'updated': now,
                'when': when,
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

    async def get_game_roadmap_links(self):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=self.spreadsheet_id,
            range='Games!A2:B'
        ).execute()

        return result.get('values', [])
