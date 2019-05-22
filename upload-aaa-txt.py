#/usr/bin/env python3
# -*- encoding: utf-8 -*- 
from __future__ import print_function
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from apiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools
import io
import hashlib
import shutil

# aaa.txt's file ID
aaaTxtFileId = "0B-ioCteW0EKSeVlmQmxCTURzVG8"

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
        print("credential not valie or found. Getting one now.")
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
        print("credential retrieved.")

    # build service
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # make a request to get aaa.txt
    request = service.files().get_media(fileId=aaaTxtFileId)

    # make a byte reader and set it up to read bytes from response
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    print("Downloading file for md5sum check.")
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

    # get md5sum of the downloaded aaa.txt
    filecontent = fh.getvalue()
    checksum = hashlib.md5(filecontent).hexdigest()

    # get md5sum of original file (.aaa.txt, which was downloaded last time)
    with open(".aaa.txt", 'rb') as org_file:
        org_checksum = hashlib.md5(org_file.read()).hexdigest()

    print("checksum of file on Google Drive: " + checksum)
    print("checksum of copy on local: " + org_checksum)
    print(type(checksum))
    print(checksum == org_checksum)
    if checksum == org_checksum:
         print("checksums matched!")
         media = MediaFileUpload("aaa.txt")
         results = service.files().update(fileId=aaaTxtFileId, media_body=media, fields="id").execute()
         if results:
             print("Upload successful.")
             shutil.copy2("aaa.txt", ".aaa.txt")
             print("copied aaa.txt to .aaa.txt")
         else:
             print("Something went wrong with upload...")
    else:
         print("checksums do not match. Exiting with no upload.")

if __name__ == '__main__':
    main()
