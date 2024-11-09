import google.auth
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd


def get_data_sheets(link:str):
    # Path to the Service Account JSON key file
    SERVICE_ACCOUNT_FILE = 'credentials.json'

    # Define the scope (read-only access for example)
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # Authenticate using the Service Account
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Build the Sheets API service
    service = build('sheets', 'v4', credentials=creds)

    # link = "https://docs.google.com/spreadsheets/d/17IMHZcWDaWOdfakrHVBI6y7h22cFz_CvBHsBMfXiGKk/edit?usp=sharing"

    # The Google Sheet ID and range
    SPREADSHEET_ID = link.split("/")[5]

    # Fetch the data
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='A:Z').execute()
    values = result.get('values', [])
    values = pd.DataFrame(values)
    return values

