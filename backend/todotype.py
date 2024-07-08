from pydantic import BaseModel




class Todo(BaseModel):
    title: str
    id: int
    category: str
    completed: bool = False