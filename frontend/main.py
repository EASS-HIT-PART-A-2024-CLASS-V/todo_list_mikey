import streamlit as st
import requests
import time

# FastAPI server URL
FASTAPI_BASE_URL = "http://backend:8000"

if 'update_triggered' not in st.session_state:
    st.session_state.update_triggered = False

st.title("Todo Tasks List")

# shows your tasks
with st.expander("Active tasks"):
    response = requests.get(f"{FASTAPI_BASE_URL}/todo/tasks")
    if response.status_code == 200:
        todos = response.json()
        if not todos:
            st.markdown("No tasks")
        else:
            for todo in todos:
                st.markdown(f" - Task ID: {todo['id']} - Task: {todo['title']} - Category: {todo['category']} - Completed: {str(todo['completed'])}", unsafe_allow_html=True)
    else:
        st.error("Failed to load tasks")

# add task
with st.form("add_task", clear_on_submit=True):
    st.subheader("Add a new task")
    new_task = st.text_input("Title")
    new_id = st.number_input("ID", value=1, format="%d")
    new_category = st.text_input("Category")
    submitted = st.form_submit_button("Add task")
    if submitted:
        todo = {"title": new_task, "id": new_id, "category": new_category, "completed": False}
        response = requests.post(f"{FASTAPI_BASE_URL}/todo/tasks", json=todo)
        if response.status_code == 200:
            time.sleep(2)
            st.success("Task added successfully!")
            st.session_state.update_triggered = True
            st.rerun()
        else:
            st.error("Failed to add task")

# Update/Delete task
with st.expander("Update/Delete task"):
    action = st.radio("Choose action:", options=["Delete task", "Update Task", "Update Completed Status"], index=0, key="action")
    task_id = st.number_input("Enter Task ID", value=1, format="%d", key="upd_del")
    task_category = st.text_input("Enter Category", key="category")

    if action == "Delete task":
        if st.button("DeleteTask", key="delete_task_btn"):
            url = f"{FASTAPI_BASE_URL}/todo/tasks/{task_category}/{task_id}"
            response = requests.delete(url)
            if response.status_code == 200:
                st.success(f"Task {task_id} deleted!")
                time.sleep(2)
                st.session_state.update_triggered = True
                st.rerun()
            else:
                st.error("Failed to delete TODO")

    if action == "Update Task":
        updated_title = st.text_input("Update Task Title", key = "title")
        if st.button("Update", key = "update_btn"):
            todo = {"title": updated_title, "id": task_id, "category": task_category, "completed": False}
            response = requests.put(f"{FASTAPI_BASE_URL}/todo/tasks/{task_category}/{task_id}", json=todo)
            if response.status_code == 200:
                st.success("Task updated successfully!")
                time.sleep(2)
                st.session_state.update_triggered = True
                st.rerun()
            else:
                st.error("Failed to update Task")


    if action == "Update Completed Status":
        new_completed_status = st.checkbox("Completed", key="completed")
        if st.button("UpdateCompleted", key="update_completed_btn"):
            url = f"{FASTAPI_BASE_URL}/todo/tasks/complete/{task_category}/{task_id}"
            response = requests.put(url, json={"completed": new_completed_status})
            if response.status_code == 200:
                st.success(f"Task {task_id} updated!")
                time.sleep(2)
                st.session_state.update_triggered = True
                st.rerun()
            else:
                st.error("Failed to update Task")

