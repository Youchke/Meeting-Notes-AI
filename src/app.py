import os
import shutil
import uuid
from typing import Dict

from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from pipelines import audio_to_summary

app = FastAPI()

# Mount static files for the frontend
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Store tasks in memory (for simplicity, in a real app use a database)
tasks: Dict[str, dict] = {}

class TaskStatus(BaseModel):
    task_id: str
    status: str
    result: dict = None
    error: str = None

import tempfile

def process_file(task_id: str, file_path: str, project_name: str, api_key: str):
    try:
        tasks[task_id]["status"] = "Processing"
        
        # Run the pipeline without saving to disk
        result = audio_to_summary(project=project_name, audio_path=file_path, api_key=api_key, save_output=False)
        
        tasks[task_id]["status"] = "Completed"
        tasks[task_id]["result"] = result
    except Exception as e:
        tasks[task_id]["status"] = "Failed"
        tasks[task_id]["error"] = str(e)
        print(f"Task {task_id} failed: {e}")
    finally:
        # Clean up the temp file
        if os.path.exists(file_path):
            os.remove(file_path)

@app.get("/")
async def read_index():
    return FileResponse("src/static/index.html")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("src/static/favicon.png")

@app.post("/api/upload")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    task_id = str(uuid.uuid4())
    project_name = "web_upload_" + task_id[:8]
    
    # Create a temp file
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        file_path = tmp.name
        
    # Get API key from environment variable
    api_key = os.environ.get("GEMINI_API_KEY")
        
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not found in environment")

    tasks[task_id] = {"status": "Pending", "result": None}
    
    background_tasks.add_task(process_file, task_id, file_path, project_name, api_key)
    
    return {"task_id": task_id}

@app.get("/api/status/{task_id}")
async def get_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]
