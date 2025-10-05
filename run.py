import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('DnD_Character_Sheet_Template_Styled')

Character_Information = SHEET.worksheet('Character Info')
Abilities = SHEET.worksheet('Abilities')
Combat = SHEET.worksheet('Combat')
Skills = SHEET.worksheet('Skills & Saves')
Equipment = SHEET.worksheet('Equipment')
Features = SHEET.worksheet('Features & Traits')
Spells = SHEET.worksheet('Spells')
Notes = SHEET.worksheet('Notes & Personality')
