import http.client

import httplib2

spread_conf = {
    "TOKEN": 'token/SpreadSheetAccessToken.json',
    "CREDENTIALS": 'credential/SpreadSheetAccessCredentials.json',
    "VERSION": 'v4',
    "SERVICE_NAME": 'sheets',
    "SCOPES": ['https://www.googleapis.com/auth/spreadsheets.readonly'],
    "BODY_RANGE": 'Sheet1!A2:G50',
    "HEADER_RANGE": 'Sheet1!A1:G1'
}

drive_conf = {
    "TOKEN": 'token/GoogleDriveAccessToken.json',
    "CREDENTIALS": 'credential/GoogleDriveAccessCredentials.json',
    "VERSION": 'v3',
    "SERVICE_NAME": 'drive',
    "SCOPES": ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets'],
}

youtube_conf = {
    "TOKEN": 'token/YouTubeAccessToken.json',
    "CREDENTIALS": 'credential/YouTubeAccessCredentials.json',
    "VERSION": 'v3',
    "SERVICE_NAME": 'youtube',
    "SCOPES": ['https://www.googleapis.com/auth/youtube.upload'],
    "RETRIABLE_EXCEPTIONS": (httplib2.HttpLib2Error,
                             IOError,
                             http.client.NotConnected,
                             http.client.IncompleteRead,
                             http.client.ImproperConnectionState,
                             http.client.CannotSendRequest,
                             http.client.CannotSendHeader,
                             http.client.ResponseNotReady,
                             http.client.BadStatusLine),
    "RETRIABLE_STATUS_CODES": [500, 502, 503, 504],
    "MAX_RETRIES": 10

}

query_conf = {"GET_FNAME_FROMDIR_ID": "parents in '[DIR_ID]'",
              "FIELD1": "nextPageToken, files(id, name, mimeType, parents, trashed)",
              "FIELD2": "nextPageToken, files(id, name)",
              "ALL": "files(*)"
              }
