from datetime import datetime
import pandas as pd
from prefect import task
from prefect.utilities.notifications import slack_notifier
from prefect import config as pconf

from model.youtube_request_param import YoutubeRequestParam


@task(name="get_upload_info", state_handlers=[slack_notifier])
def get_upload_info(client, config, _):
    def get_params_from_sheet_by_date(df, _date) -> dict:
        return df[df.date == _date].to_dict("records")

    # spreadシートからtsv中身を取得
    header = client.spread.spreadsheets().values().\
        get(spreadsheetId=pconf.context.spread.UPLOAD_LIST_ID,
            range=config["spread_conf"]["HEADER_RANGE"]).execute().get('values', [])

    body = client.spread.spreadsheets().values().\
        get(spreadsheetId=pconf.context.spread.UPLOAD_LIST_ID,
            range=config["spread_conf"]["BODY_RANGE"]).execute().get('values', [])

    params = get_params_from_sheet_by_date(
        df=pd.DataFrame(body, columns=header[0]),
        _date=datetime.now().strftime("%Y-%m-%d"))[0]

    youtube_param = YoutubeRequestParam(params=params)

    return youtube_param
