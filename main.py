from fastapi import FastAPI
import workflow.workflow as wf

app = FastAPI()

config = None
client = None


@app.on_event("startup")
async def startup_event():
    global config
    global client
    client, config = wf.initialize()


@app.get("/youtube_upload_from_gdrive")
async def youtube_upload_from_gdrive():
    """
    This function uploads your movie to youtube from your google-drive.
    - Movie is must on your google-drive and stored by today(yyyy-mm-dd) folder name.
    - Additionally, It is necessary to wrote contents on your spread-sheet already.
    """
    state = wf.youtube_upload_from_gdrive(client=client, config=config)
    return {str(k[0]): str(k[1]) for k in state.result.items()}


@app.get("/")
async def root():
    return {"/youtube_upload_from_gdrive": f"{youtube_upload_from_gdrive.__doc__}"}
