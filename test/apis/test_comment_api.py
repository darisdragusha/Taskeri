import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.app import app
from app.models.dtos.task_dtos import CommentCreate, CommentResponse, CommentListResponse
from datetime import datetime

client = TestClient(app)

def test_create_comment(authorized_client, mock_comment_response):
    """Test creating a new comment"""
    with patch('app.controllers.comment_controller.CommentController.create_comment') as mock_create:
        mock_create.return_value = mock_comment_response
        
        comment_data = {
            "task_id": 1,
            "content": "Test comment"
        }
        
        response = authorized_client.post("/comments", json=comment_data)
        assert response.status_code == 201
        assert response.json()["content"] == "Test comment"
        assert response.json()["user"]["email"] == "test@example.com"

def test_get_comment(authorized_client, mock_comment_response):
    """Test getting a comment by ID"""
    with patch('app.controllers.comment_controller.CommentController.get_comment') as mock_get:
        mock_get.return_value = mock_comment_response
        
        response = authorized_client.get("/comments/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["content"] == "Test comment"

def test_get_task_comments(authorized_client, mock_comment_response):
    """Test getting comments for a task"""
    with patch('app.controllers.comment_controller.CommentController.get_task_comments') as mock_get_task_comments:
        mock_get_task_comments.return_value = CommentListResponse(
            comments=[mock_comment_response],
            total=1,
            page=1,
            page_size=20,
            total_pages=1
        )
        
        response = authorized_client.get("/comments/task/1")
        assert response.status_code == 200
        assert response.json()["total"] == 1
        assert len(response.json()["comments"]) == 1
        assert response.json()["comments"][0]["content"] == "Test comment"

def test_update_comment(authorized_client, mock_comment_response):
    """Test updating a comment"""
    with patch('app.controllers.comment_controller.CommentController.update_comment') as mock_update:
        mock_update.return_value = mock_comment_response
        
        update_data = {
            "content": "Updated comment"
        }
        
        response = authorized_client.put("/comments/1", json=update_data)
        assert response.status_code == 200
        assert response.json()["content"] == "Test comment"

def test_delete_comment(authorized_client):
    """Test deleting a comment"""
    with patch('app.controllers.comment_controller.CommentController.delete_comment') as mock_delete:
        mock_delete.return_value = None
        
        response = authorized_client.delete("/comments/1")
        assert response.status_code == 200
        assert response.json()["message"] == "Comment deleted successfully"

def test_get_task_comments_pagination(authorized_client, mock_comment_response):
    """Test getting paginated comments for a task"""
    with patch('app.controllers.comment_controller.CommentController.get_task_comments') as mock_get_task_comments:
        mock_get_task_comments.return_value = CommentListResponse(
            comments=[mock_comment_response] * 5,
            total=15,
            page=1,
            page_size=5,
            total_pages=3
        )
        
        response = authorized_client.get("/comments/task/1?page=1&page_size=5")
        assert response.status_code == 200
        assert response.json()["total"] == 15
        assert len(response.json()["comments"]) == 5
        assert response.json()["total_pages"] == 3

def test_get_task_comments_empty(authorized_client):
    """Test getting comments for a task with no comments"""
    with patch('app.controllers.comment_controller.CommentController.get_task_comments') as mock_get_task_comments:
        mock_get_task_comments.return_value = CommentListResponse(
            comments=[],
            total=0,
            page=1,
            page_size=20,
            total_pages=0
        )
        
        response = authorized_client.get("/comments/task/1")
        assert response.status_code == 200
        assert response.json()["total"] == 0
        assert len(response.json()["comments"]) == 0
        assert len(response.json()["comments"]) == 0
