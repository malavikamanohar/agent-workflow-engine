# Agent Workflow Engine

A lightweight workflow engine for building agent-based systems with conditional routing and loops.

## Features

- **Node-based execution**: Define workflow steps as nodes with associated functions
- **State management**: Shared state dictionary flows through the workflow
- **Conditional routing**: Branch based on state values
- **Loop support**: Repeat nodes until conditions are met
- **FastAPI backend**: RESTful API for workflow management
- **Tool registry**: Register and use Python functions as workflow tools

## To Run:

1.Copy all files from the artifact above into your project directory
2.Install dependencies: pip install -r requirements.txt
3.Run the server: uvicorn app.main:app --reload --port 8000
4.Test it: Visit http://localhost:8000/docs for interactive API docs

## Project Structure

```
app/
├── __init__.py
├── main.py              # FastAPI app and endpoints
├── engine.py            # Core workflow engine
├── tools.py             # Workflow tool functions
└── workflows/
    ├── __init__.py
    └── code_review.py   # Example: Code review workflow
```

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Create a Custom Workflow
```bash
POST /graph/create
```

**Request:**
```json
{
  "name": "My Workflow",
  "nodes": {
    "node1": {
      "function": "my_tool_function"
    }
  },
  "edges": {
    "START": "node1",
    "node1": "END"
  },
  "conditional_edges": {
    "node1": {
      "check": {
        "field": "score",
        "operator": ">=",
        "value": 80,
        "target": "END"
      }
    }
  }
}
```

### 2. Run a Workflow
```bash
POST /graph/run
```

**Request:**
```json
{
  "graph_id": "uuid-here",
  "initial_state": {
    "code": "def hello():\n    print('world')"
  }
}
```

### 3. Get Run State
```bash
GET /graph/state/{run_id}
```

### 4. Create Code Review Workflow
```bash
POST /workflows/code-review/create
```

Returns a pre-configured code review workflow.

## Example: Code Review Workflow

The included code review workflow demonstrates:

1. **Extract functions**: Parse function definitions
2. **Check complexity**: Analyze code metrics
3. **Detect issues**: Find common problems
4. **Suggest improvements**: Generate recommendations
5. **Loop**: Refine until quality_score >= 80

**Usage:**
```bash
# Create the workflow
curl -X POST http://localhost:8000/workflows/code-review/create

# Run it (use returned graph_id)
curl -X POST http://localhost:8000/graph/run \
  -H "Content-Type: application/json" \
  -d '{
    "graph_id": "your-graph-id",
    "initial_state": {
      "code": "def example():\n    x = 1\n    return x"
    }
  }'
```

## Workflow Engine Capabilities

- **Sequential execution**: Nodes run in defined order
- **Conditional branching**: Route based on state values
- **Loop support**: Repeat nodes until conditions met (with max iteration safety)
- **Async execution**: Non-blocking workflow runs
- **Tool registry**: Register Python functions as reusable tools
- **Execution logging**: Track each step with timestamps

## Supported Operators

For conditional edges:
- `>=`, `>`, `<=`, `<`, `==`, `!=`

## Future Improvements

With more time, I would add:

1. **Persistent storage**: PostgreSQL/SQLite for graphs and runs
2. **WebSocket streaming**: Real-time execution updates
3. **Parallel execution**: Run independent nodes concurrently
4. **Error recovery**: Retry logic and fallback paths
5. **Graph visualization**: Visual workflow editor
6. **Advanced scheduling**: Cron-based workflow triggers
7. **State snapshots**: Save/restore workflow state at any point
8. **Plugin system**: Dynamic tool loading
9. **Validation**: Schema validation for nodes and state
10. **Monitoring**: Metrics and observability

## Design Principles

- **Simplicity**: Clean, readable code over complex abstractions
- **Extensibility**: Easy to add new tools and workflows
- **Type safety**: Pydantic models for API validation
- **Separation of concerns**: Engine, tools, and workflows are decoupled

