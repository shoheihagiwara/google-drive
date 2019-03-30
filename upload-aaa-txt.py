from __future__ import print_function
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from apiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools
import io
import hashlib

myFileId = "0B-ioCteW0EKSeVlmQmxCTURzVG8"

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', \
          'https://www.googleapis.com/auth/drive.readonly', \
          'https://www.googleapis.com/auth/drive']

def main():
    """upload aaa.txt if not modified by someone else.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')

    # get token if not already.
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    # build service
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # make a request to get aaa.txt
    request = service.files().get_media(fileId=myFileId)

    # make a byte reader and set it up to read bytes from response
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

    # get md5sum of the downloaded aaa.txt
    filecontent = fh.getvalue()
    checksum = hashlib.md5(filecontent).hexdigest()

    # get md5sum of original file (.aaa.txt, which was downloaded last time)
    with open(".aaa.txt", 'rb') as org_file:
        org_checksum = hashlib.md5(org_file.read()).hexdigest()

    print("checksum: " + checksum)
    print("org_checksum: " + org_checksum)
    print(type(checksum))
    print(checksum == org_checksum)
    if checksum == org_checksum:
         media = MediaFileUpload("aaa.txt")
         results = service.files().update(fileId=myFileId, media_body=media, fields="id").execute()
         #print(results)
         if results:
             print("Upload successful.")
         else:
             print("Something went wrong with upload...")

if __name__ == '__main__':
    main()