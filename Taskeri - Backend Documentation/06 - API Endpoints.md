# API Endpoints

## Overview

Taskeri provides a comprehensive set of RESTful API endpoints organized by resource. This document outlines all available endpoints, their required permissions, and basic request/response formats.

## Authentication Endpoints

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| POST | `/token` | Authenticate user and get JWT token | None (Public) |
| POST | `/tenant-users/` | Register a new tenant | None (Public) |

## User Management

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| POST | `/users/create` | Create a new user | `create_user` |
| GET | `/users/{user_id}` | Get user by ID | `read_user`, `read_any_user` |
| GET | `/users` | Get all users | `read_user`, `read_any_user` |
| PUT | `/users/{user_id}` | Update user | `update_user`, `update_any_user` |
| DELETE | `/users/{user_id}` | Delete user | `delete_user`, `delete_any_user` |

## Task Management

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| POST | `/tasks` | Create a new task | `create_task` |
| GET | `/tasks/{task_id}` | Get task by ID | `read_task`, `read_any_task` |
| GET | `/tasks` | Get tasks (paginated) | `read_task` |
| PUT | `/tasks/{task_id}` | Update task | `update_task`, `update_any_task` |
| DELETE | `/tasks/{task_id}` | Delete task | `delete_own_task`, `delete_any_task` |
| GET | `/tasks/{task_id}/details` | Get task details | `read_task`, `read_any_task` |
| GET | `/tasks/project/{project_id}` | Get tasks by project | `read_task` |
| GET | `/tasks/user/{user_id}` | Get tasks by user | `read_task`, `read_any_user_task` |
| GET | `/tasks/statistics` | Get task statistics | `view_statistics` |

## Project Management

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| POST | `/projects` | Create a new project | `create_project` |
| GET | `/projects/{project_id}` | Get project by ID | `read_project` |
| GET | `/projects` | Get all projects | `read_project` |
| PUT | `/projects/{project_id}` | Update project | `update_project`, `update_any_project` |
| DELETE | `/projects/{project_id}` | Delete project | `delete_project`, `delete_any_project` |
| GET | `/projects/statistics` | Get project statistics | `view_statistics` |

## Team Management

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| POST | `/teams` | Create a new team | `create_team` |
| GET | `/teams/{team_id}` | Get team by ID | `read_team` |
| GET | `/teams` | Get all teams | `read_team` |
| PUT | `/teams/{team_id}` | Update team | `update_team` |
| DELETE | `/teams/{team_id}` | Delete team | `delete_team` |
| GET | `/teams/statistics` | Get team statistics | `view_statistics` |

## Department Management

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| POST | `/departments` | Create a new department | `create_department` |
| GET | `/departments/{department_id}` | Get department by ID | `read_department` |
| GET | `/departments` | Get all departments | `read_department` |
| PUT | `/departments/{department_id}` | Update department | `update_department` |
| DELETE | `/departments/{department_id}` | Delete department | `delete_department` |

## Role & Permission Management

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| POST | `/roles` | Create a new role | `create_role` |
| GET | `/roles/{role_id}` | Get role by ID | `read_roles` |
| GET | `/roles` | Get all roles | `read_roles` |
| PUT | `/roles/{role_id}` | Update role | `update_role` |
| DELETE | `/roles/{role_id}` | Delete role | `delete_role` |
| POST | `/permissions` | Create a new permission | `create_permission` |
| GET | `/permissions/{permission_id}` | Get permission by ID | `read_permission` |
| GET | `/permissions` | Get all permissions | `read_permission` |
| PUT | `/permissions/{permission_id}` | Update permission | `update_permission` |
| DELETE | `/permissions/{permission_id}` | Delete permission | `delete_permission` |
| POST | `/role-permissions` | Assign permission to role | `manage_role_permissions` |
| GET | `/role-permissions` | Get all role permissions | `manage_role_permissions` |
| POST | `/user-roles/{user_id}/roles/{role_id}` | Assign role to user | `manage_user_roles` |
| DELETE | `/user-roles/{user_id}/roles/{role_id}` | Remove role from user | `manage_user_roles` |
| GET | `/user-roles/{user_id}/roles` | Get user's roles | `manage_user_roles` |

## Comments

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| POST | `/comments` | Create a new comment | `create_comment` |
| GET | `/comments/{comment_id}` | Get comment by ID | `read_comment` |
| GET | `/comments/task/{task_id}` | Get comments for task | `read_comment` |
| PUT | `/comments/{comment_id}` | Update comment | `update_comment` |
| DELETE | `/comments/{comment_id}` | Delete comment | `delete_comment` |

## Time Tracking

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| POST | `/time-logs` | Create a new time log | `create_time_log` |
| GET | `/time-logs/my` | Get user's time logs | `read_own_time_log` |
| GET | `/time-logs/{time_log_id}` | Get time log by ID | `read_time_log`, `read_own_time_log` |
| PUT | `/time-logs/{time_log_id}` | Update time log | `update_time_log`, `update_own_time_log` |
| DELETE | `/time-logs/{time_log_id}` | Delete time log | `delete_time_log`, `delete_own_time_log` |
| GET | `/time-logs/task/{task_id}` | Get time logs for task | `read_time_log` |
| GET | `/time-logs/user/{user_id}/by-time` | Get user logs by time range | `read_time_log`, `read_user_time_log` |

## Attendance

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| POST | `/attendance/check-in` | Check in | `check_in` |
| PUT | `/attendance/check-out` | Check out | `check_out` |
| GET | `/attendance/my` | Get user's attendance | `read_own_attendance` |
| GET | `/attendance/user/{user_id}` | Get user's attendance | `read_any_user_attendance` |

## Leave Requests

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| POST | `/leave-requests` | Create leave request | `create_leave_request` |
| GET | `/leave-requests/{leave_id}` | Get leave request by ID | `read_leave_request` |
| PATCH | `/leave-requests/{leave_id}/status` | Update leave status | `update_leave_status` |
| DELETE | `/leave-requests/{leave_id}` | Delete leave request | `delete_leave_request` |
| GET | `/leave-requests/user/{user_id}` | Get user's leave requests | `read_any_user_leave_request` |

## File Attachments

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| POST | `/attachments` | Create a new attachment | `create_attachment` |
| GET | `/attachments/{attachment_id}` | Get attachment by ID | `read_attachment` |
| GET | `/attachments` | Get all attachments | `read_attachment` |
| PUT | `/attachments/{attachment_id}` | Update attachment | `update_attachment` |
| DELETE | `/attachments/{attachment_id}` | Delete attachment | `delete_attachment` |
| GET | `/attachments/task/{task_id}` | Get attachments for task | `read_attachment` |

## Company Management

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| POST | `/companies` | Create a new company | `create_company` |
| GET | `/companies/{company_id}` | Get company by ID | `read_company` |
| GET | `/companies` | Get all companies | `read_company` |
| PUT | `/companies/{company_id}` | Update company | `update_company` |
| DELETE | `/companies/{company_id}` | Delete company | `delete_company` |

## Invoices

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| POST | `/invoices` | Create a new invoice | `create_invoice` |
| GET | `/invoices/{invoice_id}` | Get invoice by ID | `read_invoice` |
| GET | `/invoices` | Get all invoices | `read_invoice` |
| PUT | `/invoices/{invoice_id}` | Update invoice | `update_invoice` |
| DELETE | `/invoices/{invoice_id}` | Delete invoice | `delete_invoice` |

## Project User Assignment

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| POST | `/project-users` | Assign user to project | `assign_user_to_project` |
| DELETE | `/project-users` | Remove user from project | `remove_user_from_project` |
| GET | `/project-users/{project_id}/users` | Get project users | `read_project_users` |
| GET | `/project-users/users/{user_id}/projects` | Get user projects | `read_user_projects` |
| GET | `/project-users/me/projects` | Get current user's projects | `read_user_projects` |

## API Usage Examples

### Authentication

Request:
```http
POST /token HTTP/1.1
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=mysecretpassword
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    UserDetails[]
  }
}
```

### Creating a Task

Request:
```http
POST /tasks HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "title": "Implement API documentation",
  "description": "Create comprehensive API docs using Swagger",
  "status": "todo",
  "priority": "high",
  "due_date": "2023-12-31",
  "project_id": 1,
  "assigned_to": [1, 2]
}
```

Response:
```json
{
  "id": 42,
  "title": "Implement API documentation",
  "description": "Create comprehensive API docs using Swagger",
  "status": "todo",
  "priority": "high",
  "due_date": "2023-12-31",
  "project_id": 1,
  "created_by": 1,
  "created_at": "2023-10-15T14:30:00Z"
}
```