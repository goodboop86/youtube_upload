from fastapi import FastAPI
import workflow.workflow as wf
app = FastAPI()


@app.get("/youtube_upload_workflow")
async def root():
    state = wf.youtube_upload_workflow()
    return {"message": f"{state.result}"}
