```python
import json
from datetime import datetime
from pathlib import Path

def _extract_tech_stack(description: str) -> dict:
    description_lower = description.lower()
    tech_stack = {}
    
    if any(word in description_lower for word in ["fastapi", "flask", "django", "backend", "api"]):
        tech_stack["backend"] = "fastapi"
    
    if any(word in description_lower for word in ["react", "vue", "angular", "frontend", "ui"]):
        tech_stack["frontend"] = "react"
    
    if any(word in description_lower for word in ["postgres", "postgresql", "mysql", "sqlite", "database", "db"]):
        if "postgres" in description_lower:
            tech_stack["database"] = "postgresql"
        elif "mysql" in description_lower:
            tech_stack["database"] = "mysql"
        else:
            tech_stack["database"] = "sqlite"
    
    if any(word in description_lower for word in ["auth", "login", "signup", "jwt", "oauth"]):
        tech_stack["auth"] = "jwt"
    
    return tech_stack

def _generate_modules(description: str, tech_stack: dict) -> list:
    modules = []
    
    if tech_stack.get("database"):
        modules.append({
            "id": "mod_database",
            "name": "database",
            "type": "backend",
            "description": f"{tech_stack['database']} database setup with models and connection",
            "dependencies": [],
            "files": [
                {"path": "database/models.py", "type": "models"},
                {"path": "database/db.py", "type": "connection"}
            ]
        })
    
    if tech_stack.get("auth"):
        modules.append({
            "id": "mod_auth",
            "name": "auth",
            "type": "backend",
            "description": "Authentication module with login and signup",
            "dependencies": ["mod_database"] if tech_stack.get("database") else [],
            "files": [
                {"path": "auth/routes.py", "type": "router"},
                {"path": "auth/jwt.py", "type": "handler"},
                {"path": "auth/models.py", "type": "schemas"}
            ]
        })
    
    if tech_stack.get("backend"):
        deps = []
        if tech_stack.get("auth"):
            deps.append("mod_auth")
        elif tech_stack.get("database"):
            deps.append("mod_database")
        
        modules.append({
            "id": "mod_backend",
            "name": "backend",
            "type": "backend",
            "description": f"{tech_stack['backend']} main application",
            "dependencies": deps,
            "files": [
                {"path": "main.py", "type": "app"},
                {"path": "routes.py", "type": "router"}
            ]
        })
    
    if tech_stack.get("frontend"):
        modules.append({
            "id": "mod_frontend",
            "name": "frontend",
            "type": "frontend",
            "description": f"{tech_stack['frontend']} frontend application",
            "dependencies": ["mod_backend"] if tech_stack.get("backend") else [],
            "files": [
                {"path": "frontend/src/App.jsx", "type": "component"},
                {"path": "frontend/src/index.html", "type": "html"}
            ]
        })
    
    if not modules:
        modules.append({
            "id": "mod_main",
            "name": "main",
            "type": "backend",
            "description": "Main application module",
            "dependencies": [],
            "files": [
                {"path": "main.py", "type": "app"}
            ]
        })
    
    return modules

def plan_task(project_name: str, description: str) -> dict:
    tech_stack = _extract_tech_stack(description)
    modules = _generate_modules(description, tech_stack)
    
    plan = {
        "project_name": project_name,
        "version": "1.0.0",
        "description": description,
        "tech_stack": tech_stack,
        "modules": modules,
        "deployment": {
            "venv": True,
            "requirements": "auto-generate",
            "run_command": "python main.py" if not tech_stack.get("backend") == "fastapi" else "uvicorn main:app --reload",
            "tests": "pytest tests/ -v"
        },
        "created_at": datetime.utcnow().isoformat()
    }
    
    return plan

def format_plan_for_api(plan: dict) -> dict:
    return {
        "status": "success",
        "plan": {
            "project_name": plan.get("project_name"),
            "description": plan.get("description"),
            "tech_stack": plan.get("tech_stack", {}),
            "modules": [
                {
                    "id": m.get("id"),
                    "name": m.get("name"),
                    "type": m.get("type"),
                    "description": m.get("description"),
                    "dependencies": m.get("dependencies", []),
                    "files_count": len(m.get("files", []))
                }
                for m in plan.get("modules", [])
            ],
            "total_modules": len(plan.get("modules", [])),
            "deployment": plan.get("deployment", {})
        }
    }
```