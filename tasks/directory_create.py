# driveにディレクトリを自動生成する。(7 days)
# localからでも参照できるが、せっかくなのでAPIを使ってみる
from datetime import datetime, timedelta

import prefect
from prefect import task

from prefect.utilities.notifications import slack_notifier


@task(name="directory_create", state_handlers=[slack_notifier])
def directory_create(client, config, _=None):
    logger = prefect.context.get("logger")
    # ディレクトリ情報を取得
    query = config["drive_conf"]["query"]["GET_FNAME_FROMDIR_ID"].replace(
        "[DIR_ID]", config['personal_conf']['YOUTUBE_DIR_ID'])
    result = client.drive.files().list(q=query, pageSize=20,
                                       fields=config["drive_conf"]["query"]["FIELD1"]).execute().get('files', [])

    logger.info(f"Check with :  {query}")

    # 存在しているディレクトリを取得
    dirs = [elem["name"] for elem in result if
            elem['mimeType'] == 'application/vnd.google-apps.folder' and elem['trashed'] is False]

    logger.info(f"It's Already created: '{dirs}'")

    # ディレクトリ情報
    file_metadata = {
        'name': '',
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [config['personal_conf']['YOUTUBE_DIR_ID']]
    }

    # 向こう７日分を作成
    for i in range(7):
        date = datetime.now() + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        if date_str not in dirs:
            logger.info(f"Create directory : '{date}'")
            file_metadata['name'] = date_str
            client.drive.files().create(body=file_metadata, fields='id').execute()

    return _
