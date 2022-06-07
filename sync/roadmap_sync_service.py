import logging
from db.roadmap_event_repo import RoadmapEventRepo
from ekp_sdk.services import GoogleSheetsClient
from datetime import datetime

class RoadmapSyncService():
    def __init__(
        self,
        roadmap_event_repo: RoadmapEventRepo,
        google_sheets_client: GoogleSheetsClient,
        sheet_id: str
    ):
        self.roadmap_event_repo = roadmap_event_repo
        self.google_sheets_client = google_sheets_client
        self.sheet_id = sheet_id
        
    async def sync_roadmap_events(self):
        roadmap_event_values = self.google_sheets_client.get_range(self.sheet_id, 'events!A2:F')
        
        now = datetime.now().timestamp()
        
        documents = []
        
        for event_row in roadmap_event_values:
            if len(event_row) < 5:
                continue
             
            month = event_row[0]
            qtr = event_row[1]
            year = event_row[2]
            game_id = event_row[3]
            event = event_row[4]
            timestamp = None

            if not year:
                logging.warn(f"Skipping milestone for {game_id} due to missing year")
                continue
            
            year = int(year)

            description = ""
            if (len(event_row) > 5):
                description = event_row[5]
            
            if month:
                month = int(month)
                qtr = int((month / 3)) + 1
                timestamp = datetime(year,month,1)
                phase = timestamp.strftime('%b - %Y')
                timestamp = timestamp.timestamp()
            elif qtr:
                qtr = int(qtr)
                phase = f"Q{qtr} - {year}"
                month = qtr * 3
                timestamp = datetime(year,month,1).timestamp()
            else:
                logging.warn(f"Skipping milestone for {game_id} due to missing month and quarter")
                continue
            
            document = {
                'description': description,
                'event': event,
                'game_id': game_id,
                'month': month,
                'phase': phase,
                'quarter': qtr,
                'timestamp': timestamp,
                'updated': now,
                'year': year,
            }
            
            documents.append(document)
            
        self.roadmap_event_repo.save(documents)    