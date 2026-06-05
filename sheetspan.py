# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-api-python-client",
#     "google-auth-httplib2",
#     "google-auth-oauthlib",
# ]
# ///

import os
import sys
import webbrowser
import mimetypes
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

CONFIG_DIR = Path.home() / ".config" / "sheetspan"
CREDS_FILE = CONFIG_DIR / "credentials.json"
TOKEN_FILE = CONFIG_DIR / "token.json"

def get_mime_type(file_path):
    mime_type, _ = mimetypes.guess_type(str(file_path))
    if mime_type is None:
        # Fallbacks for some common types if mimetypes fails
        ext = file_path.suffix.lower()
        if ext == '.csv':
            return 'text/csv'
        elif ext in ['.xls', '.xlsx']:
            return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        elif ext == '.ods':
            return 'application/vnd.oasis.opendocument.spreadsheet'
        return 'application/octet-stream'
    return mime_type

def get_or_create_folder(service, folder_name="sheetspan"):
    query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    if not items:
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        return folder.get('id')
    return items[0].get('id')

def main():
    if len(sys.argv) < 2:
        print("Usage: uv run sheetspan.py <path_to_spreadsheet_file>")
        sys.exit(1)

    file_path = Path(sys.argv[1]).resolve()
    
    if not file_path.exists():
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    if not CREDS_FILE.exists():
        print(f"Error: Credentials file not found at {CREDS_FILE}")
        print("Please create an OAuth Client ID in Google Cloud Console (Desktop app),")
        print("download the JSON file, and save it to that location.")
        webbrowser.open("https://console.cloud.google.com/apis/credentials")
        sys.exit(1)

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        folder_id = get_or_create_folder(service, 'sheetspan')

        file_metadata = {
            'name': file_path.name,
            'mimeType': 'application/vnd.google-apps.spreadsheet',
            'parents': [folder_id]
        }
        
        source_mime_type = get_mime_type(file_path)
        
        print(f"Uploading {file_path.name} to folder 'sheetspan'...")
        media = MediaFileUpload(str(file_path), mimetype=source_mime_type, resumable=True)
        
        file = service.files().create(
            body=file_metadata, 
            media_body=media,
            fields='id, webViewLink'
        ).execute()

        web_view_link = file.get('webViewLink')
        print(f"Successfully uploaded and converted! File ID: {file.get('id')}")
        print(f"Opening in browser: {web_view_link}")
        
        # Open in default browser
        webbrowser.open(web_view_link)

    except Exception as error:
        print(f"An error occurred: {error}")
        sys.exit(1)

if __name__ == '__main__':
    main()
