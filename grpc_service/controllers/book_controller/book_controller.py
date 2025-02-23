import grpc

from grpc_service.modules.logger.logger import LoggerModule
import grpc_service.books_pb.books_pb2 as books_pb2
import grpc_service.books_pb.books_pb2_grpc as books_pb2_grpc

from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp

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
        request, 
        context,
    ):
        
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
                query
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
                
            context.set_code(grpc.StatusCode.INTERNAL)
            response = books_pb2.BookResponse()

        return response
        
    def GetAllBooks(self, request, context):
        
        connection = None
        cursor = None
        
        try:
            
            query = '''
            SELECT *
            FROM base_book
            '''
            
            self.database_controller.execute_get_query (
                query
            )
            
            books = cursor.fetchall()
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
        request, 
        context,
    ):
        
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
        request, 
        context,
    ):
        
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
        request, 
        context,
    ):

        # Validate request
        if not request.book_id:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Book ID is required for updating.")
            return books_pb2.BookResponse()

        # Generate update query and parameters
        query, params = self.build_update_query(request)

        if not query:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("No fields provided for update.")
            return books_pb2.BookResponse()

        # Append book_id to params for WHERE clause
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

            # Convert result into gRPC response
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
            self.logger.error("Database update failed: %s", str(e), exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error while updating book.")
            return books_pb2.BookResponse()
        
    def build_update_query (
        request,
    ):
        
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
