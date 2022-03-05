# driveにディレクトリを自動生成する。(7 days)
# localからでも参照できるが、せっかくなのでAPIを使ってみる
from datetime import datetime, timedelta
from prefect import task
from prefect import config as pconfig

from prefect.utilities.notifications import slack_notifier


@task(name="directory_create", state_handlers=[slack_notifier])
def directory_create(client, config) -> int:
    # ディレクトリ情報を取得
    query = config.query["GET_FNAME_FROMDIR_ID"].replace("[DIR_ID]", pconfig.context.drive.YOUTUBE_DIR_ID)
    result = client.drive.files().list(q=query, pageSize=20,
                                       fields=config.query["FIELD1"]).execute().get('files', [])

    # 存在しているディレクトリを取得
    dirs = [elem["name"] for elem in result if
            elem['mimeType'] == 'application/vnd.google-apps.folder' and elem['trashed'] is False]

    # ディレクトリ情報
    file_metadata = {
        'name': '',
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [pconfig.context.drive.YOUTUBE_DIR_ID]
    }

    # 向こう７日分を作成
    for i in range(7):
        date = datetime.now() + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        if date_str not in dirs:
            file_metadata['name'] = date_str
            client.files().create(body=file_metadata, fields='id').execute()
            print(date_str, " created.")

    return 0
