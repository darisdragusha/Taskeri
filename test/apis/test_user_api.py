import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.app import app
from app.models.dtos.user_dtos import UserCreate, UserResponse
from datetime import datetime

client = TestClient(app)

def test_create_user(authorized_client, mock_user_response):
    """Test creating a new user"""
    with patch('app.controllers.user_controller.UserController.create_user') as mock_create:
        mock_create.return_value = mock_user_response
        
        user_data = {
            "email": "new_user@example.com", # Use a different email than test fixture
            "password": "test123",
            "first_name": "Test",
            "last_name": "User",
            "department_id": None,
            "team_id": None
        }
        
        response = authorized_client.post("/users/create", json=user_data)
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"
        assert response.json()["first_name"] == "Test"

def test_get_user(authorized_client, mock_user_response):
    """Test getting a user by ID"""
    with patch('app.controllers.user_controller.UserController.get_user') as mock_get:
        mock_get.return_value = mock_user_response
        
        response = authorized_client.get("/users/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["email"] == "test@example.com"

def test_get_all_users(authorized_client, mock_user_response):
    """Test getting all users"""
    with patch('app.controllers.user_controller.UserController.get_all_users') as mock_get_all:
        mock_get_all.return_value = [mock_user_response]
        
        response = authorized_client.get("/users")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["email"] == "test@example.com"

def test_update_user(authorized_client, mock_user_response):
    """Test updating a user"""
    with patch('app.controllers.user_controller.UserController.update_user') as mock_update:
        mock_update.return_value = mock_user_response
        
        update_data = {
            "email": "updated@example.com",
            "first_name": "Updated",
            "last_name": "User",
            "department_id": None,
            "team_id": None
        }
        
        response = authorized_client.put("/users/1", json=update_data)
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"

def test_delete_user(authorized_client):
    """Test deleting a user"""
    with patch('app.controllers.user_controller.UserController.delete_user') as mock_delete:
        mock_delete.return_value = {"message": "User deleted successfully"}
        
        response = authorized_client.delete("/users/1")
        assert response.status_code == 200
        assert response.json()["message"] == "User deleted successfully"