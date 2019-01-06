from __future__ import print_function
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file, client, tools
import io

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', \
          'https://www.googleapis.com/auth/drive.readonly']

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    print(type(store))

    # get token if not already.
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    # build service
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # make a request to get aaa.txt
    request = service.files().get_media(fileId="0B-ioCteW0EKSeVlmQmxCTURzVG8")

    # make a byte reader and set it up to read bytes from response
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

    # get bytes and write out to local file named aaa.txt
    with open("aaa.txt", 'w') as aaatxt:
        aaatxt.write(fh.getvalue())

if __name__ == '__main__':
    main()
