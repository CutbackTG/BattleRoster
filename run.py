# run.py
"""
Utility module to access Google Sheets. Importing this module must NOT
attempt to open local credential files at module import time.
"""

def get_gspread_client(creds_path='creds.json'):
    """
    Returns an authorized gspread client, or raises a clear error if creds
    are unavailable. Call this from code that runs only when needed (not at import).
    """
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except Exception as e:
        raise RuntimeError("gspread/google-auth libraries are required: " + str(e))

    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    try:
        creds = Credentials.from_service_account_file(creds_path)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Google service account credentials not found at {creds_path}. "
            "On Heroku you should store credentials securely (see README)."
        )

    scoped_creds = creds.with_scopes(SCOPE)
    client = gspread.authorize(scoped_creds)
    return client


# Example usage (do NOT run on module import)
if __name__ == '__main__':
    # quick test when run locally
    client = get_gspread_client()
    sheet = client.open('DnD_Character_Sheet_Template_Styled')
    print("Works, got sheet:", sheet.title)
