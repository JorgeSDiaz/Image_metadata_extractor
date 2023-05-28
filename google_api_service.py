import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

CREDENTIALS_JSON = 'credentials.json'
CREDENTIALS = service_account.Credentials.from_service_account_file(
    CREDENTIALS_JSON,
    scopes=['https://www.googleapis.com/auth/drive.readonly']
)
DRIVE = build('drive', 'v3', credentials=CREDENTIALS)


def extract_images_from_drive_folder(folder_id: str, path: str) -> list[str]:
    file_names = []

    results = DRIVE.files().list(q=f"'{folder_id}' in parents and trashed=false",
                                 fields="files(id, name, mimeType)").execute()
    files = results.get('files', [])

    for file in files:
        file_id = file['id']
        file_name = file['name']
        mime_type = file['mimeType']

        if 'image' in mime_type:
            destination_file = path + '/' + file_name

            request = DRIVE.files().get_media(fileId=file_id)
            fh = io.FileIO(destination_file, 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Downloaded {file_name}: {int(status.progress() * 100)}%")

            print(f"Download of {file_name} complete.")
            file_names.append(file_name)

    return file_names
