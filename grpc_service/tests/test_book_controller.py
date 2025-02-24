import unittest
from unittest.mock import MagicMock
from datetime import datetime

import grpc
from dotenv import load_dotenv

from controllers.book_controller.book_controller import BookService

class TestBookService(unittest.TestCase):
    
    """
    Unit tests for the `BookService` gRPC service.

    This test suite verifies various operations such as retrieving,
    creating, updating, and deleting books using a mocked database controller.
    """
    
    def setUp (
        self,
    ) -> None:
        
        """
        Sets up the test environment before each test.

        - Loads environment variables using `dotenv`
        - Mocks the database controller
        - Initializes `BookService` with the mocked database controller
        - Mocks the gRPC context object
        """
        
        load_dotenv()
        
        self.database_controller = MagicMock()
        self.service = BookService(database_controller=self.database_controller)
        self.context = MagicMock()
    
    def test_get_book_by_id_found (
        self,
    ) -> None:
        
        """
        Tests retrieving a book by ID when the book exists.

        - Mocks a book in the database
        - Calls `GetBookById`
        - Asserts that the returned book matches the expected values
        """
        
        request = MagicMock()
        request.book_id = 1
        
        self.database_controller.execute_get_query.return_value = (1, "Book Name", "Author", datetime.utcnow())
        
        response = self.service.GetBookById (
            request, 
            self.context,
        )
        
        self.assertEqual(response.id, 1)
        self.assertEqual(response.book_name, "Book Name")
        self.assertEqual(response.author, "Author")

    def test_get_book_by_id_not_found (
        self,
    ) -> None:
        
        """
        Tests retrieving a book by ID when the book does not exist.

        - Mocks a non-existent book in the database
        - Calls `GetBookById`
        - Asserts that the response has an ID of 0 and sets the appropriate gRPC status code
        """
        
        request = MagicMock()
        request.book_id = 1
        
        self.database_controller.execute_get_query.return_value = None
        
        response = self.service.GetBookById (
            request, 
            self.context,
        )
        
        self.assertEqual(response.id, 0)
        self.context.set_code.assert_called_with(grpc.StatusCode.NOT_FOUND)
    
    def test_get_all_books (
        self,
    ) -> None:
        
        """
        Tests retrieving all books from the database.

        - Mocks a list of books in the database
        - Calls `GetAllBooks`
        - Asserts that the response contains the expected number of books
        """
        
        request = MagicMock()
        books_data = [
            (1, "Book1", "Author1", datetime.utcnow()),
            (2, "Book2", "Author2", datetime.utcnow())
        ]
        
        self.database_controller.execute_get_query.return_value = books_data
        
        response = self.service.GetAllBooks (
            request, 
            self.context,
        )
        
        self.assertEqual(len(response.books), 2)
    
    def test_post_book_success (
        self,
    ) -> None:
        
        """
        Tests adding a new book successfully.

        - Mocks a successful insert operation in the database
        - Calls `PostBook`
        - Asserts that the correct success message is set in the gRPC context
        """
        
        request = MagicMock()
        request.book_name = "New Book"
        request.book_author = "New Author"
        
        self.database_controller.execute_insert_query.return_value = 1
        
        response = self.service.PostBook(request, self.context)
        
        self.context.set_details.assert_called_with("Inserted Successfully")
    
    def test_delete_book_success (
        self,
    ) -> None:
        
        """
        Tests deleting a book successfully.

        - Calls `DeleteBook`
        - Asserts that the correct success message is set in the gRPC context
        """
        
        request = MagicMock()
        request.book_id = 1
        
        response = self.service.DeleteBook(request, self.context)
        self.context.set_details.assert_called_with("Deleted Successfully")
    
    def test_update_book_success (
        self,
    ) -> None:
        
        """
        Tests updating a book successfully.

        - Mocks a successful update operation in the database
        - Calls `UpdateBook`
        - Asserts that the returned book matches the expected updated values
        """
        
        request = MagicMock()
        request.book_id = 1
        request.book_name = "Updated Name"
        request.author = "Updated Author"
        
        self.database_controller.execute_edit_query.return_value = (1, "Updated Name", "Updated Author", datetime.utcnow())
        
        response = self.service.UpdateBook(request, self.context)
        
        self.assertEqual(response.id, 1)
        self.assertEqual(response.book_name, "Updated Name")
        self.assertEqual(response.author, "Updated Author")
    
    def test_update_book_not_found (
        self,
    ) -> None:
        
        """
        Tests updating a book that does not exist.

        - Mocks a failed update operation in the database
        - Calls `UpdateBook`
        - Asserts that the appropriate gRPC error status is set
        """
        
        request = MagicMock()
        request.book_id = 1
        request.book_name = "Updated Name"
        request.author = "Updated Author"
        
        self.database_controller.execute_edit_query.return_value = None
        
        response = self.service.UpdateBook(request, self.context)
        
        self.context.set_code.assert_called_with(grpc.StatusCode.NOT_FOUND)
        self.context.set_details.assert_called_with("Book not found.")

if __name__ == "__main__":
    unittest.main()
