# Repositories

## Overview

Repositories in Taskeri form the data access layer, abstracting database operations from the business logic. Each repository is responsible for interacting with a specific database model, providing methods for creating, reading, updating, and deleting records.

## Repository Pattern

```mermaid
classDiagram
    class Repository {
        +db_session: Session
        +__init__(db_session)
        +create()
        +get_by_id()
        +get_all()
        +update()
        +delete()
    }
```

The repository pattern provides several benefits:
- Decouples business logic from data access concerns
- Makes code more testable by allowing repository mocking
- Centralizes data access logic in dedicated classes
- Enables consistent error handling for database operations

## Key Repositories

### UserRepository

Manages user data access, including role assignments.

```mermaid
classDiagram
    class UserRepository {
        +db_session: Session
        +create_user(email, password_hash, first_name, last_name, department_id, team_id)
        +get_user_by_id(user_id)
        +get_user_by_email(email)
        +update_user(user_id, first_name, last_name, department_id, team_id)
        +delete_user(user_id)
        +assign_role_to_user(user_id, role_id)
        +remove_role_from_user(user_id, role_id)
        +get_user_roles(user_id)
        +get_role_by_name(role_name)
    }
```

### TaskRepository

Handles task data operations, including filtering and assignment.

```mermaid
classDiagram
    class TaskRepository {
        +db_session: Session
        +create_task(title, description, status, priority, due_date, project_id, created_by)
        +get_task_by_id(task_id)
        +get_all_tasks(filters, page, page_size)
        +get_tasks_by_project(project_id)
        +get_tasks_by_user(user_id)
        +update_task(task_id, update_data)
        +delete_task(task_id)
        +assign_task_to_user(task_id, user_id)
        +unassign_task_from_user(task_id, user_id)
        +get_task_statistics()
    }
```

### ProjectRepository

Manages project data and related operations.

```mermaid
classDiagram
    class ProjectRepository {
        +db_session: Session
        +create_project(name, description, start_date, end_date, owner_id)
        +get_project_by_id(project_id)
        +get_all_projects()
        +update_project(project_id, update_data)
        +delete_project(project_id)
        +assign_user_to_project(project_id, user_id)
        +remove_user_from_project(project_id, user_id)
        +get_project_users(project_id)
        +get_user_projects(user_id)
        +get_project_statistics()
    }
```

### RoleRepository

Handles role data operations.

```mermaid
classDiagram
    class RoleRepository {
        +db_session: Session
        +create_role(name)
        +create_roles_bulk(names)
        +get_role_by_id(role_id)
        +get_role_by_name(name)
        +list_roles()
        +update_role(role_id, name)
        +delete_role(role_id)
    }
```

### PermissionRepository

Manages permission data operations.

```mermaid
classDiagram
    class PermissionRepository {
        +db_session: Session
        +create_permission(name, description)
        +create_permissions_bulk(permissions_data)
        +get_permission_by_id(permission_id)
        +get_permission_by_name(name)
        +list_permissions()
        +update_permission(permission_id, update_data)
        +delete_permission(permission_id)
    }
```

### TenantUserRepository

Handles tenant user data in the global database.

```mermaid
classDiagram
    class TenantUserRepository {
        +db_session: Session
        +create(tenant_user_data)
        +get_by_id(tenant_user_id)
        +get_by_email(email)
        +get_by_tenant_schema(tenant_schema)
        +update(tenant_user_id, update_data)
        +delete(tenant_user_id)
    }
```

## Common Repository Patterns

### Constructor

Repositories accept a database session in their constructor:

```python
def __init__(self, db_session: Session):
    self.db_session = db_session
```

### CRUD Operations

Basic CRUD operations follow a consistent pattern:

```python
# Create
def create_something(self, data1, data2):
    new_entity = Entity(field1=data1, field2=data2)
    self.db_session.add(new_entity)
    self.db_session.commit()
    self.db_session.refresh(new_entity)
    return new_entity

# Read
def get_something_by_id(self, entity_id):
    return self.db_session.query(Entity).filter(Entity.id == entity_id).first()

# Update
def update_something(self, entity_id, update_data):
    entity = self.get_something_by_id(entity_id)
    if entity:
        for key, value in update_data.items():
            setattr(entity, key, value)
        self.db_session.commit()
        self.db_session.refresh(entity)
    return entity

# Delete
def delete_something(self, entity_id):
    entity = self.get_something_by_id(entity_id)
    if entity:
        self.db_session.delete(entity)
        self.db_session.commit()
    return entity
```

### Query Optimization

Repositories use join operations to optimize queries:

```python
def get_task_with_assignments(self, task_id):
    return self.db_session.query(Task)\
        .options(
            joinedload(Task.assignments).joinedload(TaskAssignment.user)
        )\
        .filter(Task.id == task_id)\
        .first()
```

### Filtering and Pagination

Methods that return multiple records often include filtering and pagination:

```python
def get_filtered_tasks(self, filters=None, page=1, page_size=20):
    query = self.db_session.query(Task)
    
    # Apply filters
    if filters:
        if filters.status:
            query = query.filter(Task.status.in_(filters.status))
        if filters.priority:
            query = query.filter(Task.priority.in_(filters.priority))
        # ...more filters
    
    # Apply pagination
    total = query.count()
    tasks = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "items": tasks,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size
    }
```

### Error Handling

Repositories use SQLAlchemy's exception handling:

```python
def create_with_error_handling(self, data):
    try:
        new_entity = Entity(**data)
        self.db_session.add(new_entity)
        self.db_session.commit()
        self.db_session.refresh(new_entity)
        return new_entity
    except SQLAlchemyError as e:
        self.db_session.rollback()
        # Let controller handle specific error
        raise e
```

## Repository Directory Structure

```
app/repositories/
├── __init__.py
├── attendance_repository.py
├── comment_repository.py
├── company_repository.py
├── department_repository.py
├── file_attachment_repository.py
├── invoice_repository.py
├── leave_request_repository.py
├── notification_repository.py
├── permission_repository.py
├── project_repository.py
├── role_permission_repository.py
├── role_repository.py
├── task_repository.py
├── team_repository.py
├── tenant_user_repository.py
├── timelog_repository.py
└── user_repository.py
```

## Testing Repositories

Repository tests typically require a test database:

```python
def test_create_user():
    # Setup test DB session
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Test repository
    repo = UserRepository(session)
    user = repo.create_user(
        email="test@example.com",
        password_hash="hashed_password",
        first_name="Test",
        last_name="User",
        department_id=None,
        team_id=None
    )
    
    # Assertions
    assert user.email == "test@example.com"
    assert user.first_name == "Test"
    
    # Check database state
    db_user = session.query(User).filter(User.email == "test@example.com").first()
    assert db_user is not None
    assert db_user.id == user.id
```