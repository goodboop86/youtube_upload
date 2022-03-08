import io
import os
from datetime import datetime
from googleapiclient.http import MediaIoBaseDownload
from prefect import task
from prefect.utilities.notifications import slack_notifier
from prefect import config as pconfig
from prefect.tasks.notifications import SlackTask


@task(name="get_upload_file", state_handlers=[slack_notifier])
def get_upload_file(client, config, _):
    # 指定IDのファイルを取得
    def get_file(_fileid, _filename, _date, _client):
        request = _client.files().get_media(fileId=_fileid)

        if not os.path.exists(_date):
            os.mkdir(_date)

        fh = io.FileIO(f"{_date}/{_filename}", 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%")

    # YOUTUBE_DIR_IDフォルダに含まれるファイルリストを取得
    query = config["drive_conf"]["query"]["GET_FNAME_FROMDIR_ID"].replace(
        "[DIR_ID]", pconfig.context.drive.YOUTUBE_DIR_ID)

    result = client.drive.files().list(q=query, pageSize=100,
                                       fields=config["drive_conf"]["query"]["FIELD1"]).execute().get('files', [])

    # 実行日のディレクトリIDを取得
    today_dir_id = [d['id'] for d in result if
                    d['name'] == datetime.now().strftime("%Y-%m-%d") and
                    d["trashed"] is False and
                    d['mimeType'] == 'application/vnd.google-apps.folder']

    # 実行日のディレクトリは１つ想定
    assert len(today_dir_id) == 1, f"expect:[1], actual[{len(today_dir_id)}]"
    today_dir_id = today_dir_id[0]

    # 実行日のディレクトリ内のファイルIDを取得
    query = config["drive_conf"]["query"]["GET_FNAME_FROMDIR_ID"].replace("[DIR_ID]", today_dir_id)
    result = client.drive.files().list(q=query, pageSize=100,
                                       fields=config["drive_conf"]["query"]["FIELD1"]).execute().get('files', [])

    # 実行日のディレクトリ内のファイルID, ファイル名を取得
    filedata = [(d['id'], d['name']) for d in result]

    # 当日ディレクトリに動画、サムネイルが保存されていない or それ以外の取得エラー
    if len(filedata) != 2:
        slack_task = SlackTask()
        slack_task.run(message=file_upload_eror.run())

    for fileid, filename in filedata:
        get_file(_fileid=fileid, _filename=filename, _date=datetime.now().strftime("%Y-%m-%d"), _client=client.drive)

    return _


@task()
def file_upload_eror():
    return "Maybe, You should save video, thumbnail-image in today's google-drive"
