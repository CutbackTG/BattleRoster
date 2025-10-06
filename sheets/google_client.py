# sheets/google_client.py
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_sheets_service():
    creds_file = getattr(settings, "GOOGLE_SERVICE_ACCOUNT_FILE", "creds.json")
    creds = service_account.Credentials.from_service_account_file(
        creds_file, scopes=SCOPES
    )
    service = build('sheets', 'v4', credentials=creds)
    return service.spreadsheets()
