from __future__ import print_function
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file, client, tools
import io

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', \
          'https://www.googleapis.com/auth/drive.readonly']

def auth():
    """authenticate to access Google Drive
    
    The file token.json stores the user's access and refresh tokens, and is
    created automatically when the authorization flow completes for the first
    time.
    """
    store = file.Storage('token.json')

    # get token if not already.
    global creds
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)


if __name__ == '__main__':
    """downlaod aaa.txt.
    This script makes two files, a copy, which will be modified and updated by a user,
    and another copy as a hidden file, which will be used for race condition checking when uploading.
    """
    
    # do authentication
    auth()

    # build service
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # make a request to get aaa.txt.
    request = service.files().get_media(fileId="0B-ioCteW0EKSeVlmQmxCTURzVG8")

    # make a byte reader and set it up to read bytes from response
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

    # get bytes and write out to local file named aaa.txt
    with open("aaa.txt", 'wb') as aaatxt:
        aaatxt.write(fh.getvalue())

    with open(".aaa.txt", "wb") as hidden:
        hidden.write(fh.getvalue())
