from __future__ import print_function

import json
import os.path
import os
from prefect import config as pconf

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from slackweb import slackweb


def get_client(conf):

    # CloudRunでcredentialなどを環境変数で設定する場合
    credentials_path = conf["CREDENTIALS"]
    credentials_env = os.getenv(conf["CREDENTIALS_ENV"])
    if credentials_env is not None:
        with open(credentials_path, mode='x') as f:
            f.write(credentials_env)

    token_path = conf["TOKEN"]
    token_env = os.getenv(conf["TOKEN_ENV"])
    if token_env is not None:
        with open(token_path, mode='x') as f:
            f.write(token_env)

    try:
        creds = None
        # The file GoogleDriveAccessToken.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(conf["TOKEN"]):
            creds = Credentials.from_authorized_user_file(conf["TOKEN"], conf["SCOPES"])
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    conf["CREDENTIALS"], conf["SCOPES"])
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(conf["TOKEN"], 'w') as token:
                token.write(creds.to_json())

        return build(conf["SERVICE_NAME"], conf["VERSION"], credentials=creds)
    except HttpError as err:
        print(err)


def slack_notify(txt):
    client = slackweb.Slack(url=pconf.context.secrets.SLACK_WEBHOOK_URL)
    client.notify(text=txt)


def dict_to_json(dic):
    return json.dumps(dic, indent=4, ensure_ascii=False)
