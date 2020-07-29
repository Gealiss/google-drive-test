from __future__ import print_function

import io
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']


def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Call the Drive v3 API
    service = build('drive', 'v3', credentials=creds)

    # upload
    file_metadata = {'name': 'photo.jpg'}
    media = MediaFileUpload('files/photo.jpg', mimetype='image/jpeg')
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    file_id = file.get('id')

    print('File ID: %s' % file_id)


if __name__ == '__main__':
    main()
