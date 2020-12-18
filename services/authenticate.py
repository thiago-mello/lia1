import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFileList
import googleapiclient.errors


SCOPES = ['https://www.googleapis.com/auth/drive.file']


def authenticate_drive_api():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if (not creds or not creds.valid):
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)
    

def get_global_folder_id(drive_service):
    return garant_folder_existence(drive_service, 'thingiverse_projects', None)

def get_project_folder_id(drive_service, project_id, global_folder_id):
    return garant_folder_existence(drive_service, project_id, global_folder_id, False)    

def garant_folder_existence(drive_service, folder_name, parent, exception_if_exists = False):
    query_str = '(mimeType = \'application/vnd.google-apps.folder\') and (name = \'{}\')'.format(folder_name)
    folder_id = get_id_if_file_exists(drive_service, query_str)
    if folder_id:
        if exception_if_exists:
            raise Exception("ja tinha pasta de projeto")
        return folder_id

    folder = create_a_folder(drive_service, folder_name, parent)
    return folder.get('id')

def get_id_if_file_exists(drive_service, query_str):
    page_token = None
    while True:
        response = drive_service.files().list(
            q=query_str,
            spaces='drive',
            fields='nextPageToken, files(id, name)',
            pageToken=page_token
        ).execute()

        for file in response.get('files', []):
            return file.get('id')

        page_token = response.get('nextPageToken', None)

        if page_token is None:
            break

def create_a_folder(drive_service, folder_name, parent):
    if parent:
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent]
        }   
    else:
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }  
    return drive_service.files().create(body=folder_metadata).execute()

def create_a_file(drive_service, file_metadata, file_media):
    return drive_service.files().create(body=file_metadata, media_body=file_media).execute()

        

