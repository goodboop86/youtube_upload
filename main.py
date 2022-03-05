from fastapi import FastAPI
import workflow.youtube_upload_from_gdrive as wf
app = FastAPI()


@app.get("/youtube_upload_workflow")
async def root():
    state = wf.youtube_upload_from_gdrive()
    return {"message": f"{state.result}"}