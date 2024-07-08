from pymongo import MongoClient
from typing import Dict, List
from functools import lru_cache

# DB connection data
@lru_cache(maxsize=None)
def get_db_connection():
    client = MongoClient("mongodb://db:27017")
    return client["todo-db"]["todo_tasks"]

def create_todo(todo_data: Dict) -> Dict:
    collection = get_db_connection()
    collection.insert_one(todo_data)
    return todo_data

def fetch_todos() -> List[Dict]:
    collection = get_db_connection()
    return list(collection.find({}, {'_id': 0}))

def update_todo(category: str, task_id: int, todo_data: Dict) -> bool:
    collection = get_db_connection()
    result = collection.update_one(
        {"category": category, "id": task_id},
        {"$set": todo_data}
    )
    return result.modified_count > 0

def delete_todo(category: str, task_id: int) -> bool:
    collection = get_db_connection()
    result = collection.delete_one({"category": category, "id": task_id})
    return result.deleted_count > 0