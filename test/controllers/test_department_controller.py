import unittest
from unittest.mock import MagicMock, patch
from app.controllers.department_controller import DepartmentController
from app.models.dtos.department_dtos import DepartmentCreate, DepartmentUpdate
from app.models.department import Department

class TestDepartmentController(unittest.TestCase):

    def setUp(self):
        self.mock_db_session = MagicMock()
        self.department_controller = DepartmentController(self.mock_db_session)

    @patch('app.repositories.department_repository.DepartmentRepository.create_department')
    def test_create_department(self, mock_create_department):
        department_data = DepartmentCreate(name="HR", company_id=1)
        mock_department = MagicMock()
        mock_department.id = 1
        mock_department.name = "HR"
        mock_department.company_id = 1
        mock_create_department.return_value = mock_department

        response = self.department_controller.create_department(department_data)

        self.assertEqual(response.name, "HR")
        self.assertEqual(response.company_id, 1)
        mock_create_department.assert_called_once_with("HR", 1)

    @patch('app.repositories.department_repository.DepartmentRepository.get_all_departments')
    def test_get_all_departments(self, mock_get_all_departments):
        mock_department1 = MagicMock()
        mock_department1.id = 1
        mock_department1.name = "HR"
        mock_department1.company_id = 1

        mock_department2 = MagicMock()
        mock_department2.id = 2
        mock_department2.name = "Finance"
        mock_department2.company_id = 1

        mock_get_all_departments.return_value = [mock_department1, mock_department2]

        response = self.department_controller.get_all_departments()

        self.assertEqual(len(response), 2)
        self.assertEqual(response[0].name, "HR")
        mock_get_all_departments.assert_called_once()

    @patch('app.repositories.department_repository.DepartmentRepository.get_department_by_id')
    def test_get_department_by_id(self, mock_get_department_by_id):
        mock_department = MagicMock()
        mock_department.id = 1
        mock_department.name = "HR"
        mock_department.company_id = 1
        mock_get_department_by_id.return_value = mock_department

        response = self.department_controller.get_department_by_id(1)

        self.assertEqual(response.name, "HR")
        self.assertEqual(response.company_id, 1)
        mock_get_department_by_id.assert_called_once_with(1)

    @patch('app.repositories.department_repository.DepartmentRepository.update_department')
    def test_update_department(self, mock_update_department):
        department_update = DepartmentUpdate(name="Updated HR")
        mock_department = MagicMock()
        mock_department.id = 1
        mock_department.name = "Updated HR"
        mock_department.company_id = 1
        mock_update_department.return_value = mock_department

        response = self.department_controller.update_department(1, department_update)

        self.assertEqual(response.name, "Updated HR")
        mock_update_department.assert_called_once_with(1, {"name": "Updated HR"})

    @patch('app.repositories.department_repository.DepartmentRepository.delete_department')
    def test_delete_department(self, mock_delete_department):
        mock_delete_department.return_value = True

        response = self.department_controller.delete_department(1)

        self.assertTrue(response)
        mock_delete_department.assert_called_once_with(1)

if __name__ == "__main__":
    unittest.main()