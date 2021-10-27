import os.path
from typing import List, Union
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import logging

logger = logging.getLogger(__name__)

class GoogleSheet:
    """
        This class creates Google Spreadsheet and append data the file.
    """
    def __init__(self) -> None:
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds = None
        self.service = self.create_service()
        self.spreadsheet = None
    
    def create_service(self):
        """
            Configurations for Google Spreadsheet operations
        """
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
    
    def create_sheet(self, spreadsheet_name: str, header: Union[List, None] = ["URL", "Product Code", "ProductName", "Availability", "Offer", "Product Price", "Sale Price"]) -> None:
        """
            Create Spreadsheet file and write header.

            Args:
                spreadsheet_name(str): File name
                header(List | None): Specifies whether there is header row in the Spreadsheet file. If header variable is None there is no header in the Spreadsheet file otherwise List of columns names.

            Returns:
                None
        """

        assert type(spreadsheet_name) == str, "spreadsheet_name variable must be str."
        assert type(header) == list or header == None, "header variable must be list or None"

        spreadsheet = {
            'properties': {
                'title': spreadsheet_name
            }
        }
        self.spreadsheet = self.service.spreadsheets().create(body=spreadsheet,
                                        fields='spreadsheetId').execute()
        if header != None:
            self.write_data(header)

        logger.info('Google Sheet is Created')
    
    def write_data(self, row: List) -> None:
        """
            Writes row the Spreadsheet file.
            
            Args:
                row(list): Data that writes the Spreadsheet file

            Returns:
                None
        """

        assert type(row) == list, "row variable must be list"

        values = [
            row
        ]
        body = {
            'values': values
        }
        
        self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet.get('spreadsheetId'), range="A1:F1",
            valueInputOption="USER_ENTERED", body=body).execute()
        
        logger.info(f'Write Data in `Markastok | Ürün Raporu`: {row}')
