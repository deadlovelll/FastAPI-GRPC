import grpc
from grpc import ServicerContext, StatusCode

from typing import Tuple, Optional
from datetime import datetime

from google.protobuf.timestamp_pb2 import Timestamp

import grpc_service.books_pb.books_pb2 as books_pb2
import grpc_service.books_pb.books_pb2_grpc as books_pb2_grpc
from grpc_service.books_pb.books_pb2 import (
    BookResponse,
    PostBookRequest,
    DeleteBookRequest,
    UpdateBookRequest,
    EmptyRequest,
    GetBookByIdRequest,
)

from grpc_service.modules.logger.logger import LoggerModule
from grpc_service.modules.database.controller.database_controller import DatabaseController
from grpc_service.controllers.base_grpc_controller.base_grpc_controller import BaseGRPCController


class BookService (
    books_pb2_grpc.BookServiceServicer, 
    BaseGRPCController,
):
    
    def __init__ (
        self,
        database_controller: DatabaseController = DatabaseController(),
    ) -> None:
        
        self.database_controller = database_controller

    def GetBookById (
        self, 
        request: GetBookByIdRequest, 
        context: ServicerContext,
    ) -> BookResponse:
        
        """
        Retrieve a book by its ID from the database.

        This method fetches a book record using the provided book ID. If the book is found,
        it returns a populated BookResponse message; if not, it sets the gRPC context with a
        NOT_FOUND status. In the event of database or unexpected errors, it rolls back the
        transaction, logs the error, and sets the gRPC context to INTERNAL.

        Args:
            request: A gRPC request object containing a 'book_id' attribute.
            context: The gRPC context used for setting error codes and details.

        Returns:
            books_pb2.BookResponse: A response message containing the book details if found,
                                    or an empty BookResponse on failure.
        """
        
        try:
            query = """
                SELECT *
                FROM base_book
                WHERE id = %s
            """
            
            book = self.database_controller.execute_get_query (
                query,
            )

            if book:
                
                response = books_pb2.BookResponse (
                    id=book[0],
                    book_name=book[1],
                    author=book[2],
                    uploaded_at=book[3],
                )
                
                ts = Timestamp()
                ts.FromDatetime(datetime.utcnow())
                response.uploaded_at.CopyFrom(ts)
            
            else:
                
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Book not found")
                
                self.logger.info("Book not found for ID: %s", request.book_id)
                
                response = books_pb2.BookResponse()

        except Exception as e:
            
            self.logger.error (
                "An unexpected error occurred: %s", 
                str(e), 
                exc_info=True,
            )
                
            context.set_code(grpc.StatusCode.INTERNAL)
            response = books_pb2.BookResponse()

        return response
        
    def GetAllBooks (
        self, 
        request: EmptyRequest, 
        context: ServicerContext,
    ) -> BookResponse:
        
        """
        Retrieves all books from the database.

        Args:
            request (EmptyRequest): The gRPC request (unused in this case).
            context (ServicerContext): The gRPC context for handling errors and status codes.

        Returns:
            BooksResponse: A response containing a list of all books in the database.

        Raises:
            StatusCode.INTERNAL: If an unexpected database error occurs.
        """
        
        try:
            
            query = '''
            SELECT *
            FROM base_book
            '''
            
            books = self.database_controller.execute_get_query (
                query
            )
            
            response = books_pb2.BooksResponse()
            
            for book in books:
                book_proto = books_pb2.BookResponse(
                    id=book[0],
                    book_name=book[1],
                    author=book[2],
                    uploaded_at=book[3]
                )
                
                ts = Timestamp()
                ts.FromDatetime(datetime.utcnow())
                book_proto.uploaded_at.CopyFrom(ts)

                response.books.append(book_proto)

        except Exception as e:
                
            self.logger.error (
                "An unexpected error occurred: %s", 
                str(e), 
                exc_info=True,
            )
            
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Unexpected error: {e}')
            
            response = books_pb2.BookResponse()
            
        return response
        
    def PostBook (
        self, 
        request: PostBookRequest, 
        context: ServicerContext,
    ) -> BookResponse:
        
        """
        Handles the creation of a new book record in the database.

        This method inserts a new book into the `base_book` table with the provided
        book name and author. The `uploaded_at` field is automatically set to the
        current timestamp.

        Args:
            request (PostBookRequest): The gRPC request containing `book_name` and `book_author`.
            context (grpc.ServicerContext): The gRPC context for setting status codes and messages.

        Returns:
            BookResponse: A gRPC response object indicating success or failure.

        Raises:
            grpc.StatusCode.INVALID_ARGUMENT: If the request does not contain required fields.
            grpc.StatusCode.INTERNAL: If an unexpected error occurs during the database operation.
        """
        
        try:
            query = '''
            INSERT INTO base_book
            (book_name, author, uploaded_at)
            VALUES (%s, %s, NOW());
            '''
            
            book_id = self.database_controller.execute_insert_query (
                query=query,
                params=(request.book_name, request.book_author)
            )
            
            if book_id:
                context.set_details('Inserted Successfully')
                response = books_pb2.BookResponse()

        except Exception as e:
            
            self.logger.error (
                "An unexpected error occurred: %s", 
                str(e), 
                exc_info=True,
            )
            
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Unexpected error: {e}')
            response = books_pb2.BookResponse()
            
        return response
        
    def DeleteBook (
        self, 
        request: DeleteBookRequest, 
        context: ServicerContext,
    )-> BookResponse:
        
        """
        Handles the deletion of a book record from the database.

        This method deletes a book from the `base_book` table based on the given `book_id`.

        Args:
            request (DeleteBookRequest): The gRPC request containing `book_id` of the book to delete.
            context (ServicerContext): The gRPC context for setting status codes and messages.

        Returns:
            BookResponse: A gRPC response object indicating success or failure.

        Raises:
            StatusCode.INVALID_ARGUMENT: If `book_id` is missing or invalid.
            StatusCode.INTERNAL: If an unexpected error occurs during the database operation.
        """
        
        try:
            query = '''
            DELETE FROM base_book
            WHERE id = %s
            '''
            
            self.database_controller.execute_delete_query (
                query,
                params=(str(request.book_id),)
            )
            
            context.set_details('Deleted Successfully')
            response = books_pb2.BookResponse()

        except Exception as e:
            self.logger.error (
                "An unexpected error occurred: %s", 
                str(e), 
                exc_info=True,
            )
            
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Unexpected error: {e}')
            response = books_pb2.BookResponse()
            
        return response
        
    def UpdateBook (
        self, 
        request: UpdateBookRequest, 
        context: ServicerContext,
    ) -> BookResponse:
        
        """
        Handles updating a book record in the database.

        Args:
            request (UpdateBookRequest): The gRPC request containing book ID and fields to update.
            context (ServicerContext): The gRPC context for handling errors and setting status codes.

        Returns:
            BookResponse: A response containing updated book details if successful.

        Raises:
            StatusCode.INVALID_ARGUMENT: If `book_id` is missing or no fields are provided for update.
            StatusCode.NOT_FOUND: If the specified book does not exist in the database.
            StatusCode.INTERNAL: If an unexpected error occurs.
        """

        if not request.book_id:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Book ID is required for updating.")
            return books_pb2.BookResponse()

        query, params = self.__build_update_query(request)

        if not query:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("No fields provided for update.")
            return books_pb2.BookResponse()

        params.append(request.book_id)
            
        try:
            updated_book = self.database_controller.execute_edit_query (
                query, 
                tuple(params),
            )

            if not updated_book:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Book not found.")
                return books_pb2.BookResponse()

            response = books_pb2.BookResponse (
                id=updated_book[0],
                book_name=updated_book[1],
                author=updated_book[2],
            )

            # Convert timestamp
            ts = Timestamp()
            ts.FromDatetime(updated_book[3])
            response.uploaded_at.CopyFrom(ts)

            return response

        except Exception as e:
            
            self.logger.error(
                "Database update failed: %s", 
                str(e), 
                exc_info=True,
            )
            
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error while updating book.")
            return books_pb2.BookResponse()
        
    def __build_update_query (
        request: UpdateBookRequest,
    ) -> Tuple[Optional[str], Optional[List[str]]]:
        
        """
        Constructs an UPDATE SQL query and parameters from the request.
        
        Args:
            request: The request object containing update fields.

        Returns:
            Tuple[str, List]: The SQL query string and corresponding parameters.
        """
        
        fields = {
            "book_name": request.book_name,
            "author": request.author,
        }

        updates = [f"{key} = %s" for key, value in fields.items() if value]
        params = [value for value in fields.values() if value]

        if not updates:
            return None, None

        query = f"UPDATE base_book SET {', '.join(updates)} WHERE id = %s"
        return query, params
