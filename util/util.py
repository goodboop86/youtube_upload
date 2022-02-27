from __future__ import print_function

import json
import os.path
from prefect import config as pconf

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from slackweb import slackweb


def get_client(conf):
    try:
        creds = None
        # The file GoogleDriveAccessToken.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(conf.get("TOKEN")):
            creds = Credentials.from_authorized_user_file(conf.get("TOKEN"), conf.get("SCOPES"))
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    conf.get("CREDENTIALS"), conf.get("SCOPES"))
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(conf.get("TOKEN"), 'w') as token:
                token.write(creds.to_json())

        return build(conf.get("SERVICE_NAME"), conf.get("VERSION"), credentials=creds)
    except HttpError as err:
        print(err)


def slack_notify(txt):
    client = slackweb.Slack(url=pconf.context.secrets.SLACK_WEBHOOK_URL)
    client.notify(text=txt)


def dict_to_json(dic):
    return json.dumps(dic, indent=4, ensure_ascii=False)
