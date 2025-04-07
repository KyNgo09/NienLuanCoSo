#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_api.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

# Đường dẫn đến file client_secrets.json
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CLIENT_SECRETS_FILE = 'client_secret.json'  

def upload_to_google_drive(file_path, file_name):
    # Xác thực
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        creds = flow.run_local_server(port=5173)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Tạo service Google Drive
    service = build('drive', 'v3', credentials=creds)

    # Tải file lên
    file_metadata = {
        'name': file_name,
        'mimeType': 'image/jpeg'  # Thay đổi nếu dùng định dạng khác (png, etc.)
    }
    media = MediaFileUpload(file_path, mimetype='image/jpeg')
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink'
    ).execute()

    # Lấy URL công khai
    file_id = file.get('id')
    file_url = file.get('webViewLink')  # URL để xem file
    return file_url