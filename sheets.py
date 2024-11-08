import google.auth
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Path to the Service Account JSON key file
SERVICE_ACCOUNT_FILE = 'credentials.json'

# Define the scope (read-only access for example)
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Authenticate using the Service Account
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Sheets API service
service = build('sheets', 'v4', credentials=creds)

# The Google Sheet ID and range
SPREADSHEET_ID = '17IMHZcWDaWOdfakrHVBI6y7h22cFz_CvBHsBMfXiGKk'

# Fetch the data
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
values = result.get('values', [])

if not values:
    print("No data found.")
else:
    for row in values:
        print(row)
# https://docs.google.com/spreadsheets/d/17IMHZcWDaWOdfakrHVBI6y7h22cFz_CvBHsBMfXiGKk/edit?usp=sharing
