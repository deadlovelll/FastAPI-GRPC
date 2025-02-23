import grpc

from grpc_service.modules.logger.logger import LoggerModule
import grpc_service.books_pb.books_pb2 as books_pb2
import grpc_service.books_pb.books_pb2_grpc as books_pb2_grpc

from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from psycopg2 import DatabaseError, OperationalError, IntegrityError, InterfaceError, ProgrammingError, DataError

class BookService(books_pb2_grpc.BookServiceServicer):
    
    def __init__ (
        self,
        logger: LoggerModule = LoggerModule(),
    ) -> None:
        
        self.logger = logger
        self.db = DBPool.get_db()

    def GetBookById (
        self, 
        request, 
        context
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
        
        connection = self.db.get_connection()
        
        try:
            with connection.cursor() as cursor:
                
                self.logger.info("Database connection established successfully.")
                
                query = """
                    SELECT *
                    FROM base_book
                    WHERE id = %s
                """
                cursor.execute (
                    query, 
                    (request.book_id,),
                )
                book = cursor.fetchone()
                
                self.logger.info("Book query executed successfully.")

            connection.commit()

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
                
                return response
            
            else:
                
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Book not found")
                
                self.logger.info("Book not found for ID: %s", request.book_id)
                
                response = books_pb2.BookResponse()

        except Exception as e:
            
            connection.rollback()
            
            if isinstance(e, self.db_exceptions):
                self.logger.fatal("Database error occurred: %s", str(e), exc_info=True)
                context.set_details(f"Database error: {e}")
            else:
                self.logger.error("An unexpected error occurred: %s", str(e), exc_info=True)
                context.set_details(f"Unexpected error: {e}")
                
            context.set_code(grpc.StatusCode.INTERNAL)
            response = books_pb2.BookResponse()

        finally:
            
            self.db.release_connection(connection)
            
            self.logger.info (
                "Database connection closed successfully."
            )

        return response
        
    def GetAllBooks(self, request, context):
        
        connection = None
        cursor = None
        
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()
            
            self.logger.info('Db connection established successfully')
            
            query = '''
            SELECT *
            FROM base_book
            '''
            
            cursor.execute(query)
            
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

        except (DatabaseError, OperationalError, IntegrityError, InterfaceError, ProgrammingError, DataError) as e:
            
            if connection:
            
                connection.rollback()
            
            self.logger.fatal(f'Database error occured: {e}. Full traceback below', exc_info=True)
            
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Database error: {e}')
            
            response = books_pb2.BookResponse()

        except Exception as e:
            
            if connection:
                
                connection.rollback()
                
            self.logger.error("An unexpected error occurred: %s", str(e), exc_info=True)
            
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Unexpected error: {e}')
            
            response = books_pb2.BookResponse()
                
        finally:
                
            cursor.close()
            self.db.release_connection(connection)
            
            self.logger.info('Db connection closed successfully')
            
            return response
        
    def PostBook(self, request, context):
        
        connection = None
        cursor = None
        
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()
            
            self.logger.info('Db connection established successfully')
            
            query = '''
            INSERT INTO base_book
            (book_name, author, uploaded_at)
            VALUES (%s, %s, NOW());
            '''
            
            cursor.execute(query, (request.book_name, request.book_author))
            
            self.logger.info('Insert query executed successfully.')

            connection.commit()
            
            context.set_details('Inserted Successfully')
            
            response = books_pb2.BookResponse()

        except (DatabaseError, OperationalError, IntegrityError, InterfaceError, ProgrammingError, DataError) as e:
            
            if connection:
            
                connection.rollback()
            
            self.logger.fatal(f'Database error occured: {e}. Full traceback below', exc_info=True)
            
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Database error: {e}')
            
            response = books_pb2.BookResponse()

        except Exception as e:
            
            if connection:
                
                connection.rollback()
                
            self.logger.error("An unexpected error occurred: %s", str(e), exc_info=True)
            
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Unexpected error: {e}')
            
            response = books_pb2.BookResponse()
                
        finally:
                
            cursor.close()
            self.db.release_connection(connection)
            
            self.logger.info('Db connection closed successfully')
            
            return response
        
    def DeleteBook(self, request, context):
        
        try:
        
            connection = self.db.get_connection()
            cursor = connection.cursor()
            
            self.logger.info('Db connection established successfully')
            
            query = '''
            DELETE FROM base_book
            WHERE id = %s
            '''
            
            cursor.execute(query, str(request.book_id))
            
            connection.commit()
            
            context.set_details('Inserted Successfully')
            
            response = books_pb2.BookResponse()
            
        except (DatabaseError, OperationalError, IntegrityError, InterfaceError, ProgrammingError, DataError) as e:
            
            if connection:
            
                connection.rollback()
            
            self.logger.fatal(f'Database error occured: {e}. Full traceback below', exc_info=True)
            
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Database error: {e}')
            
            response = books_pb2.BookResponse()

        except Exception as e:
            
            if connection:
                
                connection.rollback()
                
            self.logger.error("An unexpected error occurred: %s", str(e), exc_info=True)
            
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Unexpected error: {e}')
            
            response = books_pb2.BookResponse()
                
        finally:
                
            cursor.close()
            self.db.release_connection(connection)
            
            self.logger.info('Db connection closed successfully')
            
            return response
        
    def UpdateBook(self, request, context):
        connection = None
        cursor = None

        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()
            
            self.logger.info('Db connection established successfully')

            updates = []
            params = []

            if request.book_name:
                updates.append("book_name = %s")
                params.append(request.book_name)
            if request.author:
                updates.append("author = %s")
                params.append(request.author)

            if not updates:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("No fields provided for update.")
                return books_pb2.BookResponse()

            query = f'''
            UPDATE base_book
            SET {', '.join(updates)}
            WHERE id = %s
            '''
            params.append(request.book_id) 

            cursor.execute(query, tuple(params))
            
            connection.commit()
            
            self.logger.info('Book updated successfully.')
            
            response = books_pb2.BookResponse()
            response.id = request.book_id
            response.book_name = request.book_name if request.book_name else ''
            response.author = request.author if request.author else ''
            
        except (DatabaseError, OperationalError, IntegrityError, InterfaceError, ProgrammingError, DataError) as e:
            if connection:
                connection.rollback()
            
            self.logger.fatal(f'Database error occurred: {e}. Full traceback below', exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Database error: {e}')
            response = books_pb2.BookResponse()

        except Exception as e:
            if connection:
                connection.rollback()
            
            self.logger.error("An unexpected error occurred: %s", str(e), exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Unexpected error: {e}')
            response = books_pb2.BookResponse()
            
        finally:
            cursor.close()
            self.db.release_connection(connection)
            
            self.logger.info('Db connection closed successfully')
        
        return response