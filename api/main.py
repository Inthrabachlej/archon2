```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.orchestrator import build_project
from core.state import load_state, save_state
import os

app = FastAPI(title="Archon 2.0 API", version="2.0.0")

class BuildRequest(BaseModel):
    plan_path: str

class BuildResponse(BaseModel):
    status: str
    project_name: str
    modules_built: int
    files_created: int
    project_path: str
    errors: list = []

@app.get("/")
async def root():
    return {
        "status": "online",
        "version": "2.0.0",
        "name": "Archon 2.0 - AI Code Orchestrator"
    }

@app.post("/build", response_model=BuildResponse)
async def build(req: BuildRequest):
    """
    Build project from deployment_plan.json
    
    Args:
        plan_path: Path to deployment_plan.json (e.g., "plans/blog_api_plan.json")
    
    Returns:
        Build report with status, files created, errors
    """
    try:
        if not os.path.exists(req.plan_path):
            raise HTTPException(status_code=404, detail=f"Plan file not found: {req.plan_path}")
        
        result = build_project(req.plan_path)
        
        if result["status"] == "failed":
            raise HTTPException(status_code=500, detail={"errors": result["errors"]})
        
        return BuildResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status/{project_name}")
async def get_status(project_name: str):
    """
    Get build status and state for a project
    """
    try:
        state = load_state(project_name, "final")
        return {"status": "success", "state": state}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Project '{project_name}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/projects")
async def list_projects():
    """
    List all generated projects
    """
    try:
        projects_dir = "projects"
        if not os.path.exists(projects_dir):
            return {"projects": []}
        
        projects = [
            d for d in os.listdir(projects_dir)
            if os.path.isdir(os.path.join(projects_dir, d))
        ]
        
        return {"projects": projects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "version": "2.0.0"}
```