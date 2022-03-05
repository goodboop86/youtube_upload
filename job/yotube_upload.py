from datetime import time
from random import random
import time as tm

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from prefect import task
from prefect.utilities.notifications import slack_notifier

from util.util import slack_notify, dict_to_json


@task(name="youtube_upload", state_handlers=[slack_notifier])
def youtube_upload(client, config, params) -> list:
    def resumable_upload(insert_request, _conf):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                print("Uploading file...")  # print文
                status, response = insert_request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        print("Video id '%s' was successfully uploaded." % response['id'])
                        slack_notify(txt=f"```{response['id']}```")
                        return response['id']
                    else:
                        exit("The upload failed with an unexpected response: %s" % response)
            except HttpError as e:
                if e.resp.status in _conf.get("RETRIABLE_STATUS_CODES"):
                    error = "A retriable HTTP error %d occurred:\n%s" % \
                            (e.resp.status, e.content)
                else:
                    raise
            except _conf["RETRIABLE_EXCEPTIONS"] as e:
                error = "A retriable error occurred: %s" % e
            if error is not None:
                print(error)
                retry += 1
                if retry > _conf["MAX_RETRIES"]:
                    exit("No longer attempting to retry.")
                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                print("Sleeping %f seconds and then retrying..." % sleep_seconds)
                time.sleep(sleep_seconds)

    file, body = params
    upload_request = client.youtube.videos().insert(
        part=",".join(body.keys()),
        body=body, media_body=MediaFileUpload(f"{file}.mp4", chunksize=-1, resumable=True)
    )

    wait = 10
    txt = f"<!channel>\n" \
          f"{wait}秒後に投稿処理を行います、内容を確認して下さい。\n" \
          f"*file* \n" \
          f"```{file}```\n" \
          f"*json* \n" \
          f"```{dict_to_json(body)}```"

    slack_notify(txt=txt)
    tm.sleep(wait)

    video_id = resumable_upload(upload_request, config.youtube)
    # video_id = "dI1gE9Y4YP0"

    return [video_id, file]
