import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.app import app
from app.models.dtos.project_dtos import ProjectCreate, ProjectResponse
from datetime import datetime, date

client = TestClient(app)

def test_create_project(authorized_client, mock_project_response):
    """Test creating a new project"""
    with patch('app.controllers.project_controller.ProjectController.create_project') as mock_create:
        mock_create.return_value = mock_project_response
        
        project_data = {
            "name": "Test Project",
            "description": "A test project",
            "start_date": "2025-05-01",
            "end_date": "2025-06-01",
            "status": "In Progress",
            "assigned_user_ids": [1, 2]
        }
        
        response = authorized_client.post("/projects", json=project_data)
        assert response.status_code == 201
        assert response.json()["name"] == "Test Project"
        assert response.json()["status"] == "In Progress"

def test_get_project(authorized_client, mock_project_response):
    """Test getting a project by ID"""
    with patch('app.controllers.project_controller.ProjectController.get_project') as mock_get:
        mock_get.return_value = mock_project_response
        
        response = authorized_client.get("/projects/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["name"] == "Test Project"

def test_get_all_projects(authorized_client, mock_project_response):
    """Test getting all projects"""
    with patch('app.controllers.project_controller.ProjectController.get_all_projects') as mock_get_all:
        mock_get_all.return_value = [mock_project_response]
        
        response = authorized_client.get("/projects")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == "Test Project"

def test_update_project(authorized_client, mock_project_response):
    """Test updating a project"""
    with patch('app.controllers.project_controller.ProjectController.update_project') as mock_update:
        mock_update.return_value = mock_project_response
        
        update_data = {
            "name": "Updated Project",
            "description": "An updated project",
            "status": "Completed",
            "end_date": "2025-06-15"
        }
        
        response = authorized_client.put("/projects/1", json=update_data)
        assert response.status_code == 200
        assert response.json()["name"] == "Test Project"

def test_delete_project(authorized_client):
    """Test deleting a project"""
    with patch('app.controllers.project_controller.ProjectController.delete_project') as mock_delete:
        mock_delete.return_value = {"message": "Project deleted successfully"}
        
        response = authorized_client.delete("/projects/1")
        assert response.status_code == 200
        assert response.json()["message"] == "Project deleted successfully"

def test_get_project_statistics(authorized_client):
    """Test getting project statistics"""
    with patch('app.controllers.project_controller.ProjectController.get_project_statistics') as mock_stats:
        mock_stats.return_value = {
            "total_projects": 10,
            "completed_projects": 4,
            "in_progress_projects": 5,
            "not_started_projects": 1,
            "on_hold_projects": 0
        }
        
        response = authorized_client.get("/projects/statistics")
        assert response.status_code == 200
        assert response.json()["total_projects"] == 10
        assert response.json()["completed_projects"] == 4
