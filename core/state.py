```python
import json
import os
import shutil
from datetime import datetime
from pathlib import Path


def _get_state_path(project: str, stage: str) -> str:
    """Get path to state file for a given project and stage."""
    return f"projects/{project}/state/{stage}.json"


def save_state(stage: str, data: dict, project: str) -> None:
    """
    Save state snapshot for a given stage.
    
    Args:
        stage: Name of the stage (e.g., 'blueprint', 'module_auth')
        data: Data to save
        project: Project name
    """
    state_dir = f"projects/{project}/state"
    os.makedirs(state_dir, exist_ok=True)
    
    state_data = {
        "timestamp": datetime.now().isoformat(),
        "stage": stage,
        "data": data
    }
    
    path = _get_state_path(project, stage)
    with open(path, "w") as f:
        json.dump(state_data, f, indent=2)


def load_state(project: str, stage: str) -> dict:
    """
    Load state for a given stage.
    
    Args:
        project: Project name
        stage: Stage name
        
    Returns:
        State data dictionary
        
    Raises:
        FileNotFoundError: If state file doesn't exist
    """
    path = _get_state_path(project, stage)
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"State file not found: {path}")
    
    with open(path, "r") as f:
        return json.load(f)


def list_states(project: str) -> list:
    """
    List all saved states for a project.
    
    Args:
        project: Project name
        
    Returns:
        List of stage names
    """
    state_dir = f"projects/{project}/state"
    
    if not os.path.exists(state_dir):
        return []
    
    states = []
    for filename in os.listdir(state_dir):
        if filename.endswith(".json"):
            stage = filename[:-5]  # Remove .json extension
            states.append(stage)
    
    return sorted(states)


def delete_state(project: str, stage: str) -> bool:
    """
    Delete a specific state file.
    
    Args:
        project: Project name
        stage: Stage name
        
    Returns:
        True if deleted, False if didn't exist
    """
    path = _get_state_path(project, stage)
    
    if os.path.exists(path):
        os.remove(path)
        return True
    
    return False


def clear_all_states(project: str) -> int:
    """
    Clear all state files for a project.
    
    Args:
        project: Project name
        
    Returns:
        Number of files deleted
    """
    state_dir = f"projects/{project}/state"
    
    if not os.path.exists(state_dir):
        return 0
    
    count = 0
    for filename in os.listdir(state_dir):
        if filename.endswith(".json"):
            os.remove(os.path.join(state_dir, filename))
            count += 1
    
    return count


def get_project_status(project: str) -> dict:
    """
    Get overview of project state.
    
    Args:
        project: Project name
        
    Returns:
        Dictionary with project status info
    """
    project_dir = f"projects/{project}"
    
    if not os.path.exists(project_dir):
        return {
            "exists": False,
            "project": project
        }
    
    states = list_states(project)
    
    output_dir = f"{project_dir}/output"
    file_count = 0
    if os.path.exists(output_dir):
        for root, dirs, files in os.walk(output_dir):
            file_count += len(files)
    
    return {
        "exists": True,
        "project": project,
        "states": states,
        "state_count": len(states),
        "output_files": file_count,
        "output_dir": output_dir
    }
```