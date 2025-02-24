import unittest
from datetime import datetime
from unittest.mock import MagicMock

import grpc
from dotenv import load_dotenv

from grpc_service.controllers.book_controller.book_controller import BookService

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
        
    def test_get_book_by_id_none_returned (
        self,
    ) -> None:
        
        """
        Tests retrieving a book by ID when the database returns None for the query.
        
        - Mocks the database returning None (not found)
        - Asserts that the response is handled gracefully with status code NOT_FOUND
        """
        
        request = MagicMock()
        request.book_id = 1
        
        # Mocks database returning None
        self.database_controller.execute_get_query.return_value = None
        
        response = self.service.GetBookById (
            request, 
            self.context,
        )
        
        self.assertEqual(response.id, 0)
        self.context.set_code.assert_called_with(grpc.StatusCode.NOT_FOUND)
    
    def test_get_all_books_no_books (
        self,
    ) -> None:
        
        """
        Tests retrieving all books when there are no books in the database.
        
        - Mocks an empty database response
        - Asserts that the response contains an empty list of books
        """
        
        request = MagicMock()
        
        # Mocks an empty list of books
        self.database_controller.execute_get_query.return_value = []
        
        response = self.service.GetAllBooks (
            request, 
            self.context,
        )
        
        self.assertEqual(len(response.books), 0)
    
    def test_post_book_duplicate (
        self,
    ) -> None:
        
        """
        Tests posting a duplicate book.
        
        - Mocks a failed insert operation due to a duplicate book
        - Asserts that the appropriate error message and status code are set
        """
        
        request = MagicMock()
        request.book_name = "Duplicate Book"
        request.book_author = "Same Author"
        
        # Mocks failure due to duplicate book
        self.database_controller.execute_insert_query.side_effect = Exception("Duplicate book.")
        
        response = self.service.PostBook (
            request, 
            self.context,
        )
        
        self.context.set_code.assert_called_with(grpc.StatusCode.INTERNAL)
        self.context.set_details.assert_called_with("Unexpected error: Duplicate book.")
    
    def test_get_book_by_id_database_error (
        self,
    ) -> None:
        
        """
        Tests for database errors while fetching a book.
        
        - Mocks a database exception during the `execute_get_query`
        - Asserts that the error is logged and handled with a generic error response
        """
        
        request = MagicMock()
        request.book_id = 1
        
        # Mocks a database error
        self.database_controller.execute_get_query.side_effect = Exception("Database error")
        
        response = self.service.GetBookById (
            request, 
            self.context,
        )
        
        self.context.set_code.assert_called_with(grpc.StatusCode.INTERNAL)
        self.context.set_details.assert_called_with("Internal server error: Database error")
    
    def test_post_book_database_failure (
        self,
    ) -> None:
        
        """
        Tests posting a book when the database fails to insert the data.
        
        - Mocks a database insertion failure
        - Asserts that the appropriate error response is returned
        """
        
        request = MagicMock()
        request.book_name = "New Book"
        request.book_author = "Author Name"
        
        # Mocks failure to insert the book into the database
        self.database_controller.execute_insert_query.side_effect = Exception('Database insert failed')
        
        response = self.service.PostBook (
            request, 
            self.context,
        )
        
        self.context.set_code.assert_called_with(grpc.StatusCode.INTERNAL)
        self.context.set_details.assert_called_with('Unexpected error: Database insert failed')
    
    def test_delete_book_database_failure (
        self,
    ) -> None:
        
        """
        Tests deleting a book when the database fails to delete the book.
        
        - Mocks a failure during the deletion operation
        - Asserts that the error is handled with a generic error message
        """
        
        request = MagicMock()
        request.book_id = 1
        
        # Mocks failure to delete the book from the database
        self.database_controller.execute_delete_query.side_effect = Exception("Database delete failed.")
        
        response = self.service.DeleteBook (
            request, 
            self.context,
        )
        
        self.context.set_code.assert_called_with(grpc.StatusCode.INTERNAL)
        self.context.set_details.assert_called_with("Unexpected error: Database delete failed.")
    
    
if __name__ == "__main__":
    unittest.main()
