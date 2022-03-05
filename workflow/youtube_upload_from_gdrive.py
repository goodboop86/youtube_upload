from __future__ import print_function
import json

# DIY Package
from job.directory_create import directory_create
from job.get_upload_info import get_upload_info
from job.get_upload_file import get_upload_file
from job.upload_thumbnail import upload_thumbnail
from job.yotube_upload import youtube_upload
from model.config import Config
from model.api_client import ApiClient
from conf import conf
from util.util import get_client
from prefect import Flow
from prefect.run_configs import LocalRun


config = Config(drive=conf.drive_conf,
                spread=conf.spread_conf,
                youtube=conf.youtube_conf,
                query=conf.query_conf)

client = ApiClient(drive=get_client(config.drive),
                   spread=get_client(config.spread),
                   youtube=get_client(config.youtube))


def youtube_upload_from_gdrive():
    with Flow("YoutubeUpload") as flow:
        relay = directory_create(client=client, config=config)
        relay = get_upload_file(client=client, config=config, _=relay)
        yt_params = get_upload_info(client=client, config=config, _=relay)
        yt_params = youtube_upload(client=client, config=config, params=yt_params)
        upload_thumbnail(client=client, params=yt_params)

    flow.run_config = LocalRun(
        env={"SOME_VAR": "VALUE"},
        working_dir="../"
    )
    flow.register(project_name="YoutubeUpload")
    state = flow.run()
    return state

if __name__ == "__main__":
    state=youtube_upload_from_gdrive()
    print("done")
