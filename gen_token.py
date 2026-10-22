"""Regenerate token.pickle with full Drive scope.

Usage (on your own PC, NOT on GitHub Actions):
    pip install google-auth-oauthlib google-api-python-client
    python gen_token.py

It reads credentials.json (OAuth Desktop client from Google Cloud Console),
opens the browser for consent, then writes token.pickle in this folder.
Upload that token.pickle to your private config repo (lucnguyen06/config-files),
next to rclone.conf.

IMPORTANT: the old token was created with scope drive.file which cannot write
into a pre-existing shared folder -> 403 insufficientParentPermissions.
This script uses scope https://www.googleapis.com/auth/drive.
"""
import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/drive']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    creds_file = os.path.join(BASE_DIR, 'credentials.json')
    token_file = os.path.join(BASE_DIR, 'token.pickle')
    if not os.path.exists(creds_file):
        print(f"Missing {creds_file}.")
        print("Get it from Google Cloud Console > APIs & Services > Credentials >")
        print("Create Credentials > OAuth client ID > Desktop app, then download JSON")
        print("and save it as credentials.json next to this script.")
        raise SystemExit(1)
    flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
    creds = flow.run_local_server(port=0)
    with open(token_file, 'wb') as f:
        pickle.dump(creds, f)
    print(f"OK - wrote {token_file}")
    print("Now upload it to your private config repo (same folder as rclone.conf).")


if __name__ == '__main__':
    main()
