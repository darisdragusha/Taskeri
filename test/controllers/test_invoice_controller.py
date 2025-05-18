import unittest
from unittest.mock import MagicMock, patch
from app.controllers.invoice_controller import InvoiceController
from app.models.dtos.invoice_dtos import InvoiceCreate, InvoiceUpdate
from app.models.invoice import Invoice

class TestInvoiceController(unittest.TestCase):

    def setUp(self):
        self.mock_db_session = MagicMock()
        self.invoice_controller = InvoiceController(self.mock_db_session)

    @patch('app.repositories.invoice_repository.InvoiceRepository.create')
    def test_create_invoice(self, mock_create):
        invoice_data = InvoiceCreate(amount=100.0, description="Test Invoice", due_date="2025-05-20", company_id=1)
        mock_invoice = MagicMock()
        mock_invoice.id = 1
        mock_invoice.amount = 100.0
        mock_invoice.description = "Test Invoice"
        mock_invoice.due_date = "2025-05-20"
        mock_create.return_value = mock_invoice
        

        response = self.invoice_controller.create_invoice(invoice_data)

        self.assertEqual(response.amount, 100.0)
        self.assertEqual(response.description, "Test Invoice")
        mock_create.assert_called_once_with(invoice_data)

    @patch('app.repositories.invoice_repository.InvoiceRepository.get_all')
    def test_get_all_invoices(self, mock_get_all):
        mock_invoice1 = MagicMock()
        mock_invoice1.id = 1
        mock_invoice1.amount = 100.0
        mock_invoice1.description = "Invoice 1"

        mock_invoice2 = MagicMock()
        mock_invoice2.id = 2
        mock_invoice2.amount = 200.0
        mock_invoice2.description = "Invoice 2"

        mock_get_all.return_value = [mock_invoice1, mock_invoice2]

        response = self.invoice_controller.get_all_invoices()

        self.assertEqual(len(response), 2)
        self.assertEqual(response[0].description, "Invoice 1")
        mock_get_all.assert_called_once()

    @patch('app.repositories.invoice_repository.InvoiceRepository.get_by_id')
    def test_get_invoice_by_id(self, mock_get_by_id):
        mock_invoice = MagicMock()
        mock_invoice.id = 1
        mock_invoice.amount = 100.0
        mock_invoice.description = "Test Invoice"
        mock_get_by_id.return_value = mock_invoice

        response = self.invoice_controller.get_invoice_by_id(1)

        self.assertEqual(response.description, "Test Invoice")
        mock_get_by_id.assert_called_once_with(1)

    @patch('app.repositories.invoice_repository.InvoiceRepository.update')
    def test_update_invoice(self, mock_update):
        invoice_update = InvoiceUpdate(amount=150.0, description="Updated Invoice")
        mock_invoice = MagicMock()
        mock_invoice.id = 1
        mock_invoice.amount = 150.0
        mock_invoice.description = "Updated Invoice"
        mock_update.return_value = mock_invoice

        response = self.invoice_controller.update_invoice(1, invoice_update)

        self.assertEqual(response.amount, 150.0)
        self.assertEqual(response.description, "Updated Invoice")
        mock_update.assert_called_once_with(1, invoice_update)

    @patch('app.repositories.invoice_repository.InvoiceRepository.delete')
    def test_delete_invoice(self, mock_delete):
        mock_delete.return_value = True

        response = self.invoice_controller.delete_invoice(1)

        self.assertTrue(response)
        mock_delete.assert_called_once_with(1)

if __name__ == "__main__":
    unittest.main()