import unittest
from unittest.mock import MagicMock, patch
from app.controllers.company_controller import CompanyController
from app.models.dtos.company_dtos import CompanyCreate, CompanyUpdate

class TestCompanyController(unittest.TestCase):

    def setUp(self):
        self.mock_db_session = MagicMock()
        self.company_controller = CompanyController(self.mock_db_session)

    @patch('app.repositories.company_repository.CompanyRepository.create')
    def test_create_company(self, mock_create):
        company_data = CompanyCreate(name="Test Company", industry="Tech", country="USA")
        mock_company = MagicMock()
        mock_company.id = 1
        mock_company.name = "Test Company"
        mock_company.industry = "Tech"
        mock_company.country = "USA"
        mock_create.return_value = mock_company

        response = self.company_controller.create_company(company_data)

        self.assertEqual(response.name, "Test Company")
        self.assertEqual(response.industry, "Tech")
        mock_create.assert_called_once_with(company_data)

    @patch('app.repositories.company_repository.CompanyRepository.get_all')
    def test_get_all_companies(self, mock_get_all):
        company_a = MagicMock()
        company_a.id = 1
        company_a.name = "Company A"
        company_a.industry = "Tech"
        company_a.country = "USA"

        company_b = MagicMock()
        company_b.id = 2
        company_b.name = "Company B"
        company_b.industry = "Finance"
        company_b.country = "UK"

        mock_get_all.return_value = [company_a, company_b]

        response = self.company_controller.get_all_companies()

        self.assertEqual(len(response), 2)
        self.assertEqual(response[0].name, "Company A")
        mock_get_all.assert_called_once()

    @patch('app.repositories.company_repository.CompanyRepository.get_by_id')
    def test_get_company_by_id(self, mock_get_by_id):
        mock_company = MagicMock()
        mock_company.id = 1
        mock_company.name = "Test Company"
        mock_company.industry = "Tech"
        mock_company.country = "USA"
        mock_get_by_id.return_value = mock_company

        response = self.company_controller.get_company_by_id(1)

        self.assertEqual(response.name, "Test Company")
        self.assertEqual(response.industry, "Tech")
        mock_get_by_id.assert_called_once_with(1)

    @patch('app.repositories.company_repository.CompanyRepository.update')
    def test_update_company(self, mock_update):
        company_update = CompanyUpdate(name="Updated Company", industry="Healthcare")
        mock_company = MagicMock()
        mock_company.id = 1
        mock_company.name = "Updated Company"
        mock_company.industry = "Healthcare"
        mock_company.country = "USA"
        mock_update.return_value = mock_company

        response = self.company_controller.update_company(1, company_update)

        self.assertEqual(response.name, "Updated Company")
        self.assertEqual(response.industry, "Healthcare")
        mock_update.assert_called_once_with(1, company_update)

    @patch('app.repositories.company_repository.CompanyRepository.delete')
    def test_delete_company(self, mock_delete):
        mock_delete.return_value = True

        response = self.company_controller.delete_company(1)

        self.assertTrue(response)
        mock_delete.assert_called_once_with(1)

if __name__ == "__main__":
    unittest.main()
