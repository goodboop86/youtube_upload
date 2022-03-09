from __future__ import print_function

# DIY Package
from tasks.directory_create import directory_create
from tasks.get_upload_info import get_upload_info
from tasks.get_upload_file import get_upload_file
from tasks.upload_thumbnail import upload_thumbnail
from tasks.yotube_upload import youtube_upload
from prefect import Flow
from prefect.run_configs import LocalRun
from conf.conf import conf as conf
from util.util import secret_set, client_set


def initialize():
    status, config = secret_set.run(config=conf)
    client = client_set.run(is_cloud_operate=status, config=config)
    return client, config


def youtube_upload_from_gdrive(client, config):
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
