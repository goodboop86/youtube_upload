from googleapiclient.errors import HttpError
from prefect import task
from prefect.utilities.notifications import slack_notifier


@task(name="upload_thumbnail", state_handlers=[slack_notifier])
def upload_thumbnail(client, params):
    video_id, file = params
    try:
        res = client.thumbnails().set(
            videoId=video_id,
            media_body=f"{file}.png"
        ).execute()
        print(res)

    except HttpError as e:
        print(f"An HTTP error %d occurred:\n{(e.resp.status, e.content)}")
    else:
        print("The custom thumbnail was successfully set.")
