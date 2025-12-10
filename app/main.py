from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import uuid
from datetime import datetime

from .engine import WorkflowEngine
from .workflows.code_review import create_code_review_workflow

app = FastAPI(title="Agent Workflow Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
graphs: Dict[str, Dict] = {}
runs: Dict[str, Dict] = {}
engine = WorkflowEngine()


class GraphCreateRequest(BaseModel):
    nodes: Dict[str, Dict[str, Any]]
    edges: Dict[str, str]
    conditional_edges: Optional[Dict[str, Dict[str, Any]]] = None
    name: Optional[str] = None


class GraphRunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]


@app.post("/graph/create")
async def create_graph(request: GraphCreateRequest):
    """Create a new workflow graph"""
    graph_id = str(uuid.uuid4())
    
    graphs[graph_id] = {
        "id": graph_id,
        "name": request.name or f"Graph-{graph_id[:8]}",
        "nodes": request.nodes,
        "edges": request.edges,
        "conditional_edges": request.conditional_edges or {},
        "created_at": datetime.now().isoformat()
    }
    
    return {
        "graph_id": graph_id,
        "message": "Graph created successfully"
    }


@app.post("/graph/run")
async def run_graph(request: GraphRunRequest):
    """Execute a workflow graph"""
    if request.graph_id not in graphs:
        raise HTTPException(status_code=404, detail="Graph not found")
    
    run_id = str(uuid.uuid4())
    graph = graphs[request.graph_id]
    
    # Execute the workflow
    final_state, execution_log = await engine.run_workflow(
        nodes=graph["nodes"],
        edges=graph["edges"],
        conditional_edges=graph["conditional_edges"],
        initial_state=request.initial_state
    )
    
    # Store the run
    runs[run_id] = {
        "run_id": run_id,
        "graph_id": request.graph_id,
        "final_state": final_state,
        "execution_log": execution_log,
        "started_at": datetime.now().isoformat()
    }
    
    return {
        "run_id": run_id,
        "final_state": final_state,
        "execution_log": execution_log
    }


@app.get("/graph/state/{run_id}")
async def get_run_state(run_id: str):
    """Get the state of a specific run"""
    if run_id not in runs:
        raise HTTPException(status_code=404, detail="Run not found")
    
    return runs[run_id]


@app.get("/graphs")
async def list_graphs():
    """List all created graphs"""
    return {"graphs": list(graphs.values())}


@app.post("/workflows/code-review/create")
async def create_code_review_graph():
    """Create a pre-configured code review workflow"""
    nodes, edges, conditional_edges = create_code_review_workflow()
    
    graph_id = str(uuid.uuid4())
    graphs[graph_id] = {
        "id": graph_id,
        "name": "Code Review Workflow",
        "nodes": nodes,
        "edges": edges,
        "conditional_edges": conditional_edges,
        "created_at": datetime.now().isoformat()
    }
    
    return {
        "graph_id": graph_id,
        "message": "Code review workflow created",
        "info": "Use POST /graph/run with initial_state containing 'code' field"
    }


@app.get("/")
async def root():
    return {
        "message": "Agent Workflow Engine API",
        "endpoints": {
            "POST /graph/create": "Create a custom workflow",
            "POST /graph/run": "Execute a workflow",
            "GET /graph/state/{run_id}": "Get run state",
            "POST /workflows/code-review/create": "Create code review workflow"
        }
    }