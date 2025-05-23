import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.app import app
from app.models.dtos.task_dtos import TaskCreate, TaskResponse, TaskStatistics
from datetime import datetime, date

client = TestClient(app)

def test_create_task(authorized_client):
    """Test creating a new task"""
    with patch('app.controllers.task_controller.TaskController.create_task') as mock_create:
        mock_create.return_value = TaskResponse(
            id=1,
            project_id=1,
            name="Test Task",
            description="A test task",
            priority="High",
            status="To Do",
            due_date=date(2025, 5, 20),
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        )
        
        task_data = {
            "project_id": 1,
            "name": "Test Task",
            "description": "A test task",
            "priority": "High",
            "status": "To Do",
            "due_date": "2025-05-20",
            "assigned_user_ids": [1, 2]
        }
        
        response = authorized_client.post("/tasks", json=task_data)
        assert response.status_code == 201
        assert response.json()["name"] == "Test Task"
        assert response.json()["priority"] == "High"

def test_get_task(authorized_client):
    """Test getting a task by ID"""
    with patch('app.controllers.task_controller.TaskController.get_task') as mock_get:
        mock_get.return_value = TaskResponse(
            id=1,
            project_id=1,
            name="Test Task",
            description="A test task",
            priority="High",
            status="To Do",
            due_date=date(2025, 5, 20),
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        )
        
        response = authorized_client.get("/tasks/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["name"] == "Test Task"

def test_update_task(authorized_client):
    """Test updating a task"""
    with patch('app.controllers.task_controller.TaskController.update_task') as mock_update:
        mock_update.return_value = TaskResponse(
            id=1,
            project_id=1,
            name="Test Task",
            description="A test task",
            priority="High",
            status="To Do",
            due_date=date(2025, 5, 20),
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        )
        
        update_data = {
            "name": "Updated Task",
            "description": "An updated task",
            "status": "In Progress",
            "priority": "Medium"
        }
        
        response = authorized_client.put("/tasks/1", json=update_data)
        assert response.status_code == 200
        assert response.json()["name"] == "Test Task"

def test_delete_task(authorized_client):
    """Test deleting a task"""
    with patch('app.controllers.task_controller.TaskController.delete_task') as mock_delete:
        mock_delete.return_value = {"message": "Task deleted successfully"}
        
        response = authorized_client.delete("/tasks/1")
        assert response.status_code == 200
        assert response.json()["message"] == "Task deleted successfully"

def test_get_task_statistics(authorized_client):
    """Test getting task statistics"""
    with patch('app.controllers.task_controller.TaskController.get_task_statistics') as mock_stats:
        mock_stats.return_value = TaskStatistics(
            total_tasks=20,
            completed_tasks=8,
            in_progress_tasks=7,
            pending_tasks=5,
            high_priority_tasks=6,
            medium_priority_tasks=10,
            low_priority_tasks=4
        )
        
        response = authorized_client.get("/tasks/statistics")
        assert response.status_code == 200
        assert response.json()["total_tasks"] == 20
        assert response.json()["completed_tasks"] == 8

def test_assign_user_to_task(authorized_client):
    """Test assigning a user to a task"""
    with patch('app.controllers.task_controller.TaskController.assign_user') as mock_assign:
        mock_assign.return_value = {"message": "User assigned successfully"}
        
        response = authorized_client.post("/tasks/1/assign/2")
        assert response.status_code == 200
        assert response.json()["message"] == "User assigned successfully"

def test_get_task_assignees(authorized_client):
    """Test getting task assignees"""
    with patch('app.controllers.task_controller.TaskController.get_assignees') as mock_get:
        mock_get.return_value = [
            {"id": 1, "email": "user1@example.com", "name": "User One"},
            {"id": 2, "email": "user2@example.com", "name": "User Two"}
        ]
        
        response = authorized_client.get("/tasks/1/assignees")
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["email"] == "user1@example.com"
