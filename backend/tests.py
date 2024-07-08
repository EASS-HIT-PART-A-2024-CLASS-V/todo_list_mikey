from fastapi.testclient import TestClient
from todotype import Todo
from main import *

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "BACKEND"}



def test_update_todo_inst():
    create_response = client.post(
        "/todo/tasks",
        json={"title": "Update this title", "id": 1, "completed": False, "category": "TestToUpdate"}
    )
    assert create_response.status_code == 200
    created_todo = create_response.json()

    updated_todo = {
        "title": "Updated title",
        "completed": True,
        "category": created_todo["category"], 
        "id": created_todo["id"]  
        }

    update_response = client.put(f"/todo/tasks/{created_todo['category']}/{created_todo['id']}", json=updated_todo)
    assert update_response.status_code == 200

    get_response = client.get("/todo/tasks")
    todos = get_response.json()
    updated_todo = next((todo for todo in todos if todo["id"] == created_todo["id"] and todo["category"] == created_todo["category"]), None)

    assert updated_todo is not None
    assert updated_todo["title"] == "Updated title"
    assert updated_todo["completed"] is True
    client.delete(f"/todo/tasks/TestToUpdate/1")




def test_delete_todo():
    create_response = client.post(
        "/todo/tasks",
        json={"task": "Delete this task", "id": 999, "completed": False, "category": "TestDelete"}
    )
    assert create_response.status_code == 200
    
    delete_response = client.delete(f"/todo/tasks/TestDelete/999")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"success": "Task deleted"}

    get_response = client.get("/todo/tasks")
    todos = get_response.json()
    assert not any(todo for todo in todos if todo["id"] == 999 and todo["category"] == "TestDelete")
    