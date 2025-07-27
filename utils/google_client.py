import gspread
import os
from google.oauth2.service_account import Credentials

def google_sheets_client():
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
    SERVICE_ACCOUNT_PATH = os.path.join(PROJECT_ROOT, "resources", "google_service_account.json")

    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_PATH,
        scopes=SCOPES
    )
    client = gspread.authorize(credentials)
    return client