import unittest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from fastapi_service.main.main import app

class TestBookEndpoints(unittest.TestCase):
    
    def setUp(self):
        self.client = TestClient(app)
        self.token = "test_token"
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @patch("controllers.BookController.get_all_books", new_callable=AsyncMock)
    def test_get_all_books(self, mock_get_all_books):
        mock_get_all_books.return_value = {"books": []}
        response = self.client.get("/books/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"books": []})

    @patch("controllers.BookController.get_book_by_id", new_callable=AsyncMock)
    def test_get_book_by_id(self, mock_get_book_by_id):
        mock_get_book_by_id.return_value = {"id": 1, "name": "Test Book"}
        response = self.client.get("/books/1", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 1, "name": "Test Book"})
    
    @patch("controllers.BookController.create_book", new_callable=AsyncMock)
    def test_post_book(self, mock_create_book):
        mock_create_book.return_value = {"id": 1, "name": "New Book"}
        data = {"book_name": "New Book", "book_author": "Author"}
        response = self.client.post("/books/", json=data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 1, "name": "New Book"})

    @patch("controllers.BookController.edit_book", new_callable=AsyncMock)
    def test_edit_book(self, mock_edit_book):
        mock_edit_book.return_value = {"id": 1, "name": "Updated Book"}
        data = {"book_name": "Updated Book", "book_author": "New Author"}
        response = self.client.patch("/books/1", json=data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 1, "name": "Updated Book"})

    @patch("controllers.BookController.delete_book", new_callable=AsyncMock)
    def test_delete_book(self, mock_delete_book):
        mock_delete_book.return_value = {"message": "Book deleted"}
        response = self.client.delete("/books/1", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Book deleted"})

if __name__ == "__main__":
    unittest.main()
