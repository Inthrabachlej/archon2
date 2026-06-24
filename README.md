# ARCHON 2.0

AI-assisted software generation system for turning structured prompts into project files, modules, and implementation plans.

---

## Overview

ARCHON 2.0 orchestrates two AI models to build modular software:
- **GPT-4o** (Architect) - Generates step-by-step instructions
- **Claude Sonnet 4.5** (Builder) - Generates actual code

### Key Features
- Reads structured `deployment_plan.json`
- Validates code (syntax, imports, dependencies)
- Integrates modules (fixes imports, proper structure)
- Deploys automatically (venv, dependencies, tests)
- Outputs: **fully working, modular projects**

---

## Quick Start

### 1. Installation
```bash
git clone <repository>
cd Archon2
pip install -r requirements.txt
```

### 2. Configure API Keys
Create `.env` file:
```ini
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o

ANTHROPIC_API_KEY=sk-ant-api03-...
ANTHROPIC_MODEL=claude-sonnet-4-5-20250929
ANTHROPIC_VERSION=2023-06-01
```

### 3. Create a Deployment Plan
Example `deployment_plan.json`:
```json
{
  "project_name": "blog_api",
  "version": "1.0.0",
  "description": "FastAPI blog with JWT auth",
  "tech_stack": {
    "backend": "fastapi",
    "database": "sqlite",
    "auth": "jwt"
  },
  "modules": [
    {
      "id": "mod_database",
      "name": "database",
      "type": "backend",
      "description": "SQLite database with User and Post models",
      "dependencies": [],
      "files": [
        {"path": "database/models.py", "type": "sqlalchemy_models"},
        {"path": "database/db.py", "type": "database_connection"}
      ]
    }
  ],
  "deployment": {
    "venv": true,
    "requirements": "auto-generate",
    "run_command": "uvicorn main:app --reload",
    "tests": "pytest tests/ -v"
  }
}
```

### 4. Build Project
```bash
python cli/main.py build --plan deployment_plan.json
```

---

## Architecture

```
Archon2/
├── core/
│   ├── orchestrator.py      # Main coordination logic
│   ├── plan_parser.py       # Reads & validates deployment plans
│   ├── architect.py         # GPT-4o instruction generator
│   ├── builder.py           # Claude code generator
│   ├── validator.py         # Syntax & import checker
│   ├── integrator.py        # Module linker (fixes imports)
│   ├── deployer.py          # Venv + pip install + tests
│   ├── state.py             # State management
│   └── planner.py           # High-level task planner
├── templates/
│   └── deployment_plan.schema.json
├── api/
│   └── main.py              # FastAPI REST interface
├── cli/
│   └── main.py              # Command-line interface
├── projects/                # Generated projects
└── requirements.txt
```

---

## Execution Flow

```
1. User creates deployment_plan.json
   ↓
2. orchestrator.build_project(plan_path)
   ↓
3. plan_parser: load + validate + sort by dependencies
   ↓
4. FOR EACH module (in dependency order):
   ├─ architect (GPT-4o): generate detailed instructions
   ├─ builder (Claude): generate code
   ├─ validator: check syntax + imports
   ├─ IF errors → retry with fixes (max 2 attempts)
   └─ Save files
   ↓
5. integrator: fix imports between modules
   ↓
6. deployer: create venv → install deps → run tests
   ↓
7. Return: Working project + build report
```

---

## API Usage

### Start API Server
```bash
uvicorn api.main:app --reload --port 8000
```

### Endpoints

#### `POST /plan_task`
Generate high-level build plan (no API calls, deterministic)
```json
{
  "project_name": "my_app",
  "description": "FastAPI blog with authentication"
}
```

Response:
```json
{
  "status": "success",
  "plan": {
    "modules": [...],
    "execution_order": [...],
    "estimated_files": 12
  }
}
```

#### `POST /build`
Build complete project from deployment plan
```json
{
  "plan_path": "deployment_plan.json"
}
```

---

## CLI Usage

### Build from Plan
```bash
python cli/main.py build --plan deployment_plan.json
```

### Validate Plan
```bash
python cli/main.py validate --plan deployment_plan.json
```

### List Projects
```bash
python cli/main.py list
```

---

## Module System

### Modular Design
- Backend/frontend/auth as reusable building blocks
- Generate separately or combine together
- Swap out components (different frontend, same backend)

### Dependencies
- Modules declare dependencies via `"dependencies": ["mod_id"]`
- Automatic topological sort ensures correct build order
- No circular dependencies allowed

### Integration
- Automatic import fixing between modules
- `__init__.py` generation for proper Python packages
- Cross-module reference resolution

---

## Deployment

### Virtual Environment
- Automatically creates `venv/` per project
- Isolated dependencies per project

### Requirements
- Auto-generates `requirements.txt` from module imports
- Installs via `pip install -r requirements.txt`

### Testing
- Runs tests via `pytest` after build
- Validates module functionality
- Reports pass/fail status

---

## State Management

All build state saved to `projects/{project_name}/state/`:
- `blueprint.json` - Initial plan breakdown
- `module_{name}.json` - Per-module generation state
- `integration.json` - Import fixes and package structure
- `deployment.json` - Venv and dependency installation

### Resume/Rollback
```python
from core.state import load_state, save_state

state = load_state("integration", "my_project")
```

---

## Examples

See `templates/` directory for example deployment plans:
- `blog_api_plan.json` - FastAPI blog with JWT auth
- `todo_app_plan.json` - Full-stack todo app
- `payment_service_plan.json` - Stripe integration service

---

## Development Status

**Current Phase:** Phase 1 - Core Infrastructure
- ✅ State management
- ✅ High-level planner
- ⏳ Plan parser
- ⏳ Orchestrator
- ⏳ Architect (GPT-4o)
- ⏳ Builder (Claude)
- ⏳ Validator
- ⏳ Integrator
- ⏳ Deployer

**Target:** 5 days to working MVP

---

## Requirements

- Python 3.11+
- OpenAI API key (GPT-4o access)
- Anthropic API key (Claude Sonnet 4.5 access)
- Linux/macOS (tested on Ubuntu/Mint)

---

## License

MIT

---

## Support

For issues, feature requests, or questions, please open an issue on GitHub.