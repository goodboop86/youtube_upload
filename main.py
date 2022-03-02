from __future__ import print_function

# DIY Package
from job.directory_create import directory_create
from job.get_upload_info import get_upload_info
from job.upload_thumbnail import upload_thumbnail
from job.yotube_upload import youtube_upload
from model import config
from conf import conf
from util import util
from prefect import Flow
from prefect import config as pconf
from prefect.run_configs import LocalRun

spread_conf = config.Config(conf.spread_conf)
drive_conf = config.Config(conf.drive_conf)
youtube_conf = config.Config(conf.youtube_conf)
query_conf = config.Config(conf.query_conf)

spread_client = util.get_client(spread_conf)
drive_client = util.get_client(drive_conf)
youtube_client = util.get_client(youtube_conf)

with Flow("YoutubeUpload") as flow:
    status = directory_create(client=drive_client, conf=query_conf)
    params = get_upload_info(client=spread_client, conf=spread_conf, status=status)
    params = youtube_upload(client=youtube_client, conf=youtube_conf, params=params)
    upload_thumbnail(client=youtube_client, params=params)

flow.run_config = LocalRun(
    env={"SOME_VAR": "VALUE"},
    working_dir="./"
)
flow.register(project_name="YoutubeUpload")
flow.run()
