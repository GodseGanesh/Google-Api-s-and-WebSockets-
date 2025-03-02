import os
import json
import google.auth
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from django.conf import settings

def get_drive_service(access_token):
    """Initialize Google Drive API service using OAuth token."""
    creds = Credentials(token=access_token)
    return build('drive', 'v3', credentials=creds)

def upload_file_to_drive(access_token, file_path, file_name, mime_type):
    """Upload a file to Google Drive."""
    service = get_drive_service(access_token)
    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, mimetype=mime_type)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

def list_drive_files(access_token):
    """Fetch files from the user's Google Drive."""
    service = get_drive_service(access_token)
    results = service.files().list(fields="files(id, name)").execute()
    return results.get('files', [])

def download_file_from_drive(access_token, file_id, destination_path):
    """Download a file from Google Drive."""
    service = get_drive_service(access_token)
    request = service.files().get_media(fileId=file_id)
    with open(destination_path, "wb") as file:
        file.write(request.execute())
    return destination_path
