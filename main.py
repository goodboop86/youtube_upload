from fastapi import FastAPI
import workflow.youtube_upload_from_gdrive as wf

from model.config import Config
from model.api_client import ApiClient
from conf import conf
from util.util import get_client

app = FastAPI()

config = Config(drive=conf.drive_conf,
                spread=conf.spread_conf,
                youtube=conf.youtube_conf,
                query=conf.query_conf)

client = ApiClient(drive=get_client(config.drive),
                   spread=get_client(config.spread),
                   youtube=get_client(config.youtube))


@app.get("/youtube_upload_from_gdrive")
async def root():
    state = wf.youtube_upload_from_gdrive(client=client, config=config)
    return {"message": f"{state.result}"}
