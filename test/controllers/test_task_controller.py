import unittest
from unittest.mock import MagicMock, patch
from app.controllers.task_controller import TaskController
from app.models.dtos import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse, TaskStatistics
from datetime import date

class TestTaskController(unittest.TestCase):

    def setUp(self):
        self.mock_db_session = MagicMock()
        self.task_controller = TaskController(self.mock_db_session)

    @patch('app.repositories.task_repository.TaskRepository.create_task')
    def test_create_task(self, mock_create_task):
        task_data = TaskCreate(
            project_id=1,
            name="Test Task",
            description="A test task",
            priority="High",
            status="To Do",
            due_date=date(2025, 5, 20),
            assigned_user_ids=[1, 2]
        )
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.name = "Test Task"
        mock_task.description = "A test task"
        mock_task.priority = "High"
        mock_task.status = "To Do"
        mock_task.due_date = date(2025, 5, 20)
        mock_task.created_at = "2025-05-18T10:00:00"
        mock_task.updated_at = "2025-05-18T10:00:00"
        mock_create_task.return_value = mock_task

        response = self.task_controller.create_task(task_data)

        self.assertEqual(response.name, "Test Task")
        self.assertEqual(response.priority, "High")
        mock_create_task.assert_called_once_with(
            project_id=1,
            name="Test Task",
            description="A test task",
            priority="High",
            status="To Do",
            due_date=date(2025, 5, 20),
            assigned_user_ids=[1, 2]
        )

    @patch('app.repositories.task_repository.TaskRepository.get_task_by_id')
    def test_get_task(self, mock_get_task_by_id):
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.name = "Test Task"
        mock_task.description = "A test task"
        mock_task.priority = "High"
        mock_task.status = "To Do"
        mock_task.due_date = date(2025, 5, 20)
        mock_task.created_at = "2025-05-18T10:00:00"
        mock_task.updated_at = "2025-05-18T10:00:00"
        mock_get_task_by_id.return_value = mock_task

        response = self.task_controller.get_task(1)

        self.assertEqual(response.name, "Test Task")
        mock_get_task_by_id.assert_called_once_with(1)

    @patch('app.repositories.task_repository.TaskRepository.get_tasks_by_project')
    def test_get_tasks_by_project(self, mock_get_tasks_by_project):
        mock_task1 = MagicMock()
        mock_task1.id = 1
        mock_task1.name = "Task 1"
        mock_task1.description = "Description 1"
        mock_task1.priority = "Medium"
        mock_task1.status = "In Progress"
        mock_task1.due_date = date(2025, 5, 21)
        mock_task1.created_at = "2025-05-18T10:00:00"
        mock_task1.updated_at = "2025-05-18T10:00:00"

        mock_task2 = MagicMock()
        mock_task2.id = 2
        mock_task2.name = "Task 2"
        mock_task2.description = "Description 2"
        mock_task2.priority = "Low"
        mock_task2.status = "To Do"
        mock_task2.due_date = date(2025, 5, 22)
        mock_task2.created_at = "2025-05-18T10:00:00"
        mock_task2.updated_at = "2025-05-18T10:00:00"

        mock_get_tasks_by_project.return_value = [mock_task1, mock_task2]

        response = self.task_controller.get_tasks_by_project(1)

        self.assertEqual(len(response), 2)
        self.assertEqual(response[0].name, "Task 1")
        mock_get_tasks_by_project.assert_called_once_with(1)

    @patch('app.repositories.task_repository.TaskRepository.update_task')
    def test_update_task(self, mock_update_task):
        task_update = TaskUpdate(name="Updated Task")
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.name = "Updated Task"
        mock_task.description = "Updated Description"
        mock_task.priority = "High"
        mock_task.status = "In Progress"
        mock_task.due_date = date(2025, 5, 23)
        mock_task.created_at = "2025-05-18T10:00:00"
        mock_task.updated_at = "2025-05-18T10:00:00"
        mock_update_task.return_value = mock_task

        response = self.task_controller.update_task(1, task_update)

        self.assertEqual(response.name, "Updated Task")
        mock_update_task.assert_called_once_with(task_id=1, update_data={"name": "Updated Task"}, assigned_user_ids=None)

    @patch('app.repositories.task_repository.TaskRepository.delete_task')
    def test_delete_task(self, mock_delete_task):
        mock_delete_task.return_value = True

        response = self.task_controller.delete_task(1)

        self.assertEqual(response["message"], "Task deleted successfully")
        mock_delete_task.assert_called_once_with(1)

    @patch('app.repositories.task_repository.TaskRepository.get_task_statistics')
    def test_get_task_statistics(self, mock_get_task_statistics):
        mock_statistics = TaskStatistics(
            total_tasks=18,
            completed_tasks=3,
            overdue_tasks=2,
            tasks_by_status={"To Do": 5, "In Progress": 10, "Completed": 3},
            tasks_by_priority={"Low": 4, "Medium": 8, "High": 6}
        )
        mock_get_task_statistics.return_value = mock_statistics

        response = self.task_controller.get_task_statistics()

        self.assertEqual(response.total_tasks, 18)
        self.assertEqual(response.completed_tasks, 3)
        self.assertEqual(response.overdue_tasks, 2)
        self.assertEqual(response.tasks_by_status["To Do"], 5)
        self.assertEqual(response.tasks_by_priority["High"], 6)
        mock_get_task_statistics.assert_called_once()

if __name__ == "__main__":
    unittest.main()