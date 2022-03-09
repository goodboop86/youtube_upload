from __future__ import print_function

import json
import os.path
import os
import prefect

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from prefect import task

from model.api_client import ApiClient


def get_client_by_local(conf):
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


def get_client_by_cloud(conf):
    try:
        creds = None
        if os.path.exists(conf["TOKEN"]):
            creds = Credentials.from_authorized_user_file(conf["TOKEN"], conf["SCOPES"])

        return build(conf["SERVICE_NAME"], conf["VERSION"], credentials=creds)
    except HttpError as err:
        print(err)


@task(name="secret_set")
def secret_set(config):
    def write_file(_value, _path):
        with open(path, mode='x') as fp:
            fp.write(_value)
        os.chmod(path, 0o755)

    logger = prefect.context.get("logger")

    # conf/conf.py で取り扱えない情報
    env_path = {'GOOGLEDRIVE_ACCESS_TOKEN': 'token/googledrive-access-token.json',
                'SPREADSHEET_ACCESS_TOKEN': 'token/spreadsheet-access-token.json',
                'YOUTUBE_ACCESS_TOKEN': 'token/youtube-access-token.json',
                'PERSONAL_CONF': 'credential/personal-conf.json'}

    # 環境変数が存在するなら内容を保存する
    is_cloud_operate = False
    for env in env_path:
        path = env_path[env]
        if os.path.exists(path):
            logger.info(f"Already exists : {path}")
        else:
            if os.getenv(env) is None:
                logger.info(f"'{env}' os None.")
                raise Exception
            else:
                logger.info(f"Write it to : '{env}' -> '{path}'")
                write_file(_value=os.getenv(env), _path=path)
                is_cloud_operate = True

    # personal-conf
    with open('credential/personal-conf.json') as f:
        config['personal_conf'] = json.load(f)

    return is_cloud_operate, config


@task(name="client_set")
def client_set(is_cloud_operate, config):

    # googleAPI周りのセット
    get_client = get_client_by_cloud if is_cloud_operate else get_client_by_local

    client = ApiClient(drive=get_client(config["drive_conf"]),
                       spread=get_client(config["spread_conf"]),
                       youtube=get_client(config["youtube_conf"]))
    return client


def dict_to_json(dic):
    return json.dumps(dic, indent=4, ensure_ascii=False)
