import os
import json
import gspread
from google.oauth2.service_account import Credentials

# --- Connect to Google Sheets ---
def get_gsheet(sheet_name: str):
    creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(
        creds_dict,
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
    )
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key("14ProN3lR8p-t9j2P7b76JBOwEIrvntHqCVBee1q6bNk")
    return spreadsheet.worksheet(sheet_name)
