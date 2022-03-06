import http.client
import httplib2

drive_conf = {
    "CREDENTIALS": 'credential/googledrive-access-credentials.json',
    "CREDENTIALS_ENV": 'GOOGLEDRIVE_ACCESS_CREDENTIALS',
    "TOKEN": 'token/googledrive-access-token.json',
    "TOKEN_ENV": 'SPREADSHEET_ACCESS_TOKEN',
    "VERSION": 'v3',
    "SERVICE_NAME": 'drive',
    "SCOPES": ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets'],
}

spread_conf = {
    "CREDENTIALS": 'credential/spreadsheet-access-credentials.json',
    "CREDENTIALS_ENV": 'SPREADSHEET_ACCESS_CREDENTIALS',
    "TOKEN": 'token/spreadsheet-access-token.json',
    "TOKEN_ENV": 'GOOGLEDRIVE_ACCESS_TOKEN',
    "VERSION": 'v4',
    "SERVICE_NAME": 'sheets',
    "SCOPES": ['https://www.googleapis.com/auth/spreadsheets.readonly'],
    "BODY_RANGE": 'Sheet1!A2:G50',
    "HEADER_RANGE": 'Sheet1!A1:G1'
}

youtube_conf = {
    "CREDENTIALS": 'credential/youtube-access-credentials.json',
    "CREDENTIALS_ENV": 'YOUTUBE_ACCESS_CREDENTIALS',
    "TOKEN": 'token/youtube-access-token.json',
    "TOKEN_ENV": 'YOUTUBE_ACCESS_TOKEN',
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
