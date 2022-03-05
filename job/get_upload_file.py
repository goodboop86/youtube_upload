from datetime import datetime
import pandas as pd
from prefect import task
from prefect.utilities.notifications import slack_notifier
from prefect import config as pconf


@task(name="get_upload_info", state_handlers=[slack_notifier])
def get_upload_file(client, config, status):
    def get_params_from_sheet_by_date(df, _date) -> dict:
        return df[df.date == _date].to_dict("records")

    def create_youtube_request_param(_params, _conf):
        _file = "{}{}/{}".format(pconf.context.ABSOLUTE_DRIVE_PATH, _params["date"], _params["file"])
        privacy_status = {"privacyStatus": _params["privacyStatus"]}
        del _params['file'], _params['date'], _params['privacyStatus']

        return _file, {"snippet": _params, "status": privacy_status}

    # spreadシートからtsv中身を取得
    header = client.spread.spreadsheets().values().get(spreadsheetId=pconf.context.spread.UPLOAD_LIST_ID,
                                                       range=config.spread.get("HEADER_RANGE")).execute().get('values', [])

    body = client.spread.spreadsheets().values().get(spreadsheetId=pconf.context.spread.UPLOAD_LIST_ID,
                                                     range=config.spread.get("BODY_RANGE")).execute().get('values', [])

    query = config.query.get("GET_FNAME_FROMDIR_ID").replace("[DIR_ID]", pconf.context.drive.YOUTUBE_DIR_ID)
    result = client.drive.files().list(q=query, pageSize=20,
                                 fields=config.query.get("FIELD1")).execute().get('files', [])

    params = get_params_from_sheet_by_date(
        df=pd.DataFrame(body, columns=header[0]),
        _date=datetime.now().strftime("%Y-%m-%d"))[0]

    file, body = create_youtube_request_param(params, config.youtube)

    return [file, body]
