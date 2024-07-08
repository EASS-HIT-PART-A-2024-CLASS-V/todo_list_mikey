# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from db import create_todo, fetch_todos, update_todo, delete_todo
from todotype import Todo


app = FastAPI()



@app.get("/")
async def read_root():
    return {"message": "BACKEND"}

@app.get("/todo/tasks", response_model=List[Todo])
def get_todos():
    todos = fetch_todos()
    return todos

@app.post("/todo/tasks", response_model=Todo)
def create_todo_inst(todo: Todo):
    created_todo = create_todo(todo.model_dump())
    return created_todo


@app.put("/todo/tasks/{category}/{task_id}", response_model=Todo)
def update_todo_inst(category: str, task_id: int, todo: Todo):
    if not update_todo(category, task_id, todo.model_dump()):
        raise HTTPException(status_code=404, detail="Can't find task")
    return todo

@app.put("/todo/tasks/complete/{category}/{task_id}")
def complete_todo_inst(category: str, task_id: int):
    if not update_todo(category, task_id, {"completed": True}):
        raise HTTPException(status_code=404, detail="Can't find task")
    return {"note": "Task completed"}

@app.delete("/todo/tasks/{category}/{task_id}")
def delete_todo_inst(category: str, task_id: int):
    if not delete_todo(category, task_id):
        raise HTTPException(status_code=404, detail="Can't find task")
    return {"note": "Task deleted"}


