import gspread
from google.oauth2.service_account import Credentials

def google_sheets_client():
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    SERVICE_ACCOUNT_PATH = "../resources/google_service_account.json"
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_PATH,
        scopes=SCOPES
    )
    client = gspread.authorize(credentials)
    return client