from __future__ import print_function
import os.path
import sys
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from constants import TOKEN_PATH, CREDENTIALS_PATH, GDRIVE_FOLDER

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']
mime_folder_type = 'application/vnd.google-apps.folder'


def get_g_drive_file_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    g_file_service = build('drive', 'v3', credentials=creds).files()

    # Check if folder exists in Google Drive
    query = f"name='{GDRIVE_FOLDER}' and mimeType='{mime_folder_type}'"
    response = g_file_service.list(
        q=query,
        spaces='drive'
    ).execute()

    folder_id = None
    dirs = response.get('files', [])
    if len(dirs) != 0:
        folder_id = dirs[0].get('id')
        print(f"{GDRIVE_FOLDER} exists on current Google Drive")
        print(f"Folder Id: {folder_id}")
    else:
        # Create Folder to Google Drive if it does not exist
        print(f"{GDRIVE_FOLDER} does not exist on the current Google Drive")
        print("Creating New...")

        file_metadata = {
            'name': GDRIVE_FOLDER,
            'mimeType': mime_folder_type
        }
        file = g_file_service.create(body=file_metadata,
                                     fields='id').execute()
        folder_id = file.get('id')
        print(f"Successfully Created \nFolder Id: {folder_id}")

    return g_file_service, folder_id


def g_drive_file_upload(g_file_service, folder_id, src, desc=None):
    if not desc:
        firstpos = src.rfind("\\")
        lastpos = len(src)
        desc = src[firstpos + 1: lastpos]
    print(f"Uploading file {desc}...")

    body = {'parents': [folder_id], 'name': desc}
    media = MediaFileUpload(src)
    file = g_file_service.create(body=body, media_body=media).execute()

    print(f"Uploaded Successfully: {file.get('name')} id {file.get('id')}.")


if __name__ == '__main__':
    main()
