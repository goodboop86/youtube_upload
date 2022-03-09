import prefect
from googleapiclient.errors import HttpError
from prefect import task
from prefect.utilities.notifications import slack_notifier

from util.util import dict_to_json


@task(name="upload_thumbnail", state_handlers=[slack_notifier])
def upload_thumbnail(client, params):
    logger = prefect.context.get("logger")

    # video_id, file = params
    try:
        res = client.youtube.thumbnails().set(
            videoId=params.mov_id,
            media_body=params.img_png
        ).execute()
        logger.info(dict_to_json(res))

    except HttpError as e:
        print(f"An HTTP error %d occurred:\n{(e.resp.status, e.content)}")
    else:
        print("The custom thumbnail was successfully set.")

    logger.info("Done Upload thumbnail.")