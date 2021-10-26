from __future__ import print_function
import os.path
from typing import List
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

class GoogleSheet:
    def __init__(self) -> None:
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds = None
        self.service = self.create_service()
        self.spreadsheet = None
    
    def create_service(self):
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.scopes)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.scopes)
                self.creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        service = build('sheets', 'v4', credentials=self.creds)

        return service
    
    def create_sheet(self, sheet_name, rows: List = ["URL", "ProductName", "Availability", "Offer", "Product Price", "Sale Price"]):
        spreadsheet = {
            'properties': {
                'title': sheet_name
            }
        }
        self.spreadsheet = self.service.spreadsheets().create(body=spreadsheet,
                                        fields='spreadsheetId').execute()

        self.write_data(rows)
    
    def write_data(self, row):
        values = [
            row
        ]
        body = {
            'values': values
        }
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet.get('spreadsheetId'), range="A1:F1",
            valueInputOption="USER_ENTERED", body=body).execute()
