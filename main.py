# server.py
from mcp.server.fastmcp import FastMCP
from typing import Optional

# Create the MCP server
mcp = FastMCP("ToDo List MCP")

# In-memory task store
tasks = {}
task_counter = 1


@mcp.tool()
def add_task(description: str) -> dict:
    """Add a new task to the list"""
    global task_counter
    task_id = task_counter
    tasks[task_id] = {
        "id": task_id,
        "description": description,
        "completed": False
    }
    task_counter += 1
    return tasks[task_id]


@mcp.tool()
def list_tasks() -> list[dict]:
    """List all tasks"""
    return list(tasks.values())


@mcp.tool()
def update_task(task_id: int, description: Optional[str] = None, completed: Optional[bool] = None) -> dict:
    """Update task details (description or completed status)"""
    if task_id not in tasks:
        return {"error": "Task not found."}

    if description is not None:
        tasks[task_id]["description"] = description
    if completed is not None:
        tasks[task_id]["completed"] = completed

    return tasks[task_id]


@mcp.tool()
def delete_task(task_id: int) -> str:
    """Delete a task by ID"""
    if task_id in tasks:
        del tasks[task_id]
        return f"Task {task_id} deleted."
    return "Task not found."
