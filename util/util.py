from __future__ import print_function

import json
import os.path
import os


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


from model.api_client import ApiClient


def get_client_by_local(conf):
    # CloudRunでcredentialなどを環境変数で設定する場合
    credentials_path = conf["CREDENTIALS"]
    credentials_env = os.getenv(conf["CREDENTIALS_ENV"])
    if credentials_env is not None:
        with open(credentials_path, mode='x') as f:
            f.write(credentials_env)
        os.chmod(credentials_path, 0o755)

    token_path = conf["TOKEN"]
    token_env = os.getenv(conf["TOKEN_ENV"])
    if token_env is not None:
        with open(token_path, mode='x') as f:
            f.write(token_env)
        os.chmod(token_path, 0o755)

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
    # CloudRunでcredentialなどを環境変数で設定する場合
    token_path = conf["TOKEN"]
    token_env = os.getenv(conf["TOKEN_ENV"])
    if token_env is not None:
        with open(token_path, mode='x') as f:
            f.write(token_env)
        os.chmod(token_path, 0o755)

    try:
        creds = None
        if os.path.exists(conf["TOKEN"]):
            creds = Credentials.from_authorized_user_file(conf["TOKEN"], conf["SCOPES"])

        return build(conf["SERVICE_NAME"], conf["VERSION"], credentials=creds)
    except HttpError as err:
        print(err)


def secret_set(config):
    """
    :param config:
    dict(
        "***_conf":
            dict(
                "TOKEN_ENV":"SOME_TOKEN_VALUE"
                )
        )
    :return: boolean
    """
    def write_token(_value, _path):
        with open(path, mode='x') as f:
            f.write(_value)
        os.chmod(path, 0o755)

    token_env = "TOKEN_ENV"
    token = "token"
    token_env_names = []
    token_path = []

    # configからmountされている可能性のある環境変数名(conf[token_env])と保存先(conf[token])を取得
    for conf in config.values():
        if token_env in conf:
            token_env_names.append(conf[token_env])
        if token in conf:
            token_path.append(conf[token])

    # 環境変数が存在するなら内容を保存する
    is_cloud_operate = False
    for name, path in zip(token_env_names, token_path):
        if os.getenv(name) is not None:
            write_token(_value=os.getenv(name), _path=path)
            # クラウド環境ではclientの取得方法が異なる
            is_cloud_operate = True

    return is_cloud_operate


def client_set(is_cloud_operate, config):
    get_client = get_client_by_cloud if is_cloud_operate else get_client_by_local

    client = ApiClient(drive=get_client(config["drive_conf"]),
                       spread=get_client(config["spread_conf"]),
                       youtube=get_client(config["youtube_conf"]))
    return client


def dict_to_json(dic):
    return json.dumps(dic, indent=4, ensure_ascii=False)
