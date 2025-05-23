import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.app import app
from datetime import datetime
from sqlalchemy import text

def test_login_success(client, test_user, test_db):
    """Test successful login with correct credentials"""
    login_data = {
        "username": "test@example.com",
        "password": "password123"
    }
    
    # Ensure we are using the global DB for login
    test_db.execute(text('USE taskeri_global'))
    
    response = client.post("/token", data=login_data)
    
    # Log details for debugging - keep this temporarily
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client, test_user, test_db):
    """Test login with invalid credentials"""
    login_data = {
        "username": "test@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/token", data=login_data)
    
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Invalid credentials"

def test_login_missing_fields(client, test_db):
    """Test login with missing required fields"""
    login_data = {
        "username": "test@example.com"
        # missing password
    }
    response = client.post("/token", data=login_data)
    
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

def test_register_tenant_user(client, test_db):
    """Test registering a new tenant user"""
    user_data = {
        "email": "newuser@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User",
        "company_name": "Test Company"
    }
    response = client.post("/tenant-users", json=user_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "tenant_schema" in data

def test_register_tenant_user_email_exists(client, test_user, test_db):
    """Test registering a user with existing email"""
    user_data = {
        "email": "test@example.com",  # This email already exists
        "password": "password123",
        "first_name": "Test",
        "last_name": "User",
        "company_name": "Test Company"
    }
    response = client.post("/tenant-users", json=user_data)
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already exists" in data["detail"].lower()

def test_register_tenant_user_invalid_data(client, test_db):
    """Test registering a tenant user with invalid data"""
    user_data = {
        "email": "invalid-email",  # invalid email format
        "password": "123",  # too short password
        "first_name": "",  # empty first name
        "last_name": "User",
        "company_name": "Test Company"
    }
    response = client.post("/tenant-users", json=user_data)
    
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

def test_protected_route_without_token(client, test_db):
    """Test accessing a protected route without token"""
    response = client.get("/users/1")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_protected_route_invalid_token(client, test_db):
    """Test accessing a protected route with invalid token"""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/users/1", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired token"
