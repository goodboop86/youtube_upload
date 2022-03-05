from datetime import datetime
import pandas as pd
from prefect import task
from prefect.utilities.notifications import slack_notifier
from prefect import config as pconf

from model.youtube_param import YoutubeParam


@task(name="get_upload_info", state_handlers=[slack_notifier])
def get_upload_info(client, config, _):
    def get_params_from_sheet_by_date(df, _date) -> dict:
        return df[df.date == _date].to_dict("records")

    def create_youtube_request_param(_params):
        _file = "{}{}/{}".format(pconf.context.ABSOLUTE_DRIVE_PATH, _params["date"], _params["file"])
        privacy_status = {"privacyStatus": _params["privacyStatus"]}
        del _params['file'], _params['date'], _params['privacyStatus']

        return _file, {"snippet": _params, "status": privacy_status}

    # spreadシートからtsv中身を取得
    header = client.spread.spreadsheets().values().get(spreadsheetId=pconf.context.spread.UPLOAD_LIST_ID,
                                                       range=config.spread["HEADER_RANGE"]).execute().get('values', [])
    body = client.spread.spreadsheets().values().get(spreadsheetId=pconf.context.spread.UPLOAD_LIST_ID,
                                                     range=config.spread["BODY_RANGE"]).execute().get('values', [])

    params = get_params_from_sheet_by_date(
        df=pd.DataFrame(body, columns=header[0]),
        _date=datetime.now().strftime("%Y-%m-%d"))[0]

    youtube_param = YoutubeParam(params=params)
    # file, body = create_youtube_request_param(params)

    return youtube_param
