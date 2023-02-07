import os
from config import Config
from auction_item import AuctionItem
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class AuctionSpreadsheet:
    def __init__(self) -> None:
        scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
        self.sheet_id = Config.get_spreadsheet_id()
        self.range = "Prices!B2:D"

        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and
        # is created automatically when the authorization flow completes for
        # the first time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file(
                'token.json', scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", scopes)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

    def get_auction_items(self):
        try:
            service = build("sheets", "v4", credentials=self.creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.sheet_id,
                                        range=self.range).execute()
            values = result.get("values", [])

            if not values:
                print("No data found.")
                return

            auction_items = []
            for row in values:
                auction_item = AuctionItem(row[0], int(row[1]), int(row[2]))
                auction_items.append(auction_item)

            return auction_items
        except HttpError as err:
            print(err)
            return None
