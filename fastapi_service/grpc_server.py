import os 
import sys
import grpc
import books_pb2 as books_pb2
import books_pb2_grpc as books_pb2_grpc
import psycopg2

from psycopg2 import DatabaseError, OperationalError, IntegrityError, InterfaceError, ProgrammingError, DataError
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime
from concurrent import futures

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from modules.base_controller import BaseController
from modules.logger import LoggerModel
from modules.database_controller import DatabasePoolController

Logger = LoggerModel()
logger = Logger.logger_initialization()
DBPool = DatabasePoolController(logger=logger)

class BookService(books_pb2_grpc.BookServiceServicer):
    
    def __init__(self):
        
        self.logger = logger
        self.db = DBPool.get_db()
        
    def get_book_by_id(self, request, context):
        
        response = None
        
        try:
            
            connection = self.db.get_connection()
            cursor = connection.cursor()
            
            self.logger.info('Db connection established successfully')
            
            query = '''
            SELECT * 
            
            FROM base_book
            
            WHERE id = %s
            '''
            
            cursor.execute(query, (request.book_id,))
            
            book = cursor.fetchone()
            
            self.logger.info('Book query executed successfully')
            
            connection.commit()
            
            if book:
                
                response = books_pb2.BookResponse(
                    id=book[0],
                    book_name=book[1],
                    author=book[2],
                    uploaded_at=book[3]
                )
                
                ts = Timestamp()
                ts.FromDatetime(datetime.utcnow())
                response.uploaded_at.CopyFrom(ts)
                
                return response
            
            else:
                
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Book not found')
                
                self.logger.info('Book not found')
                
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
            
            
def serve():    
    # logger = LoggerModel()
    # db_pool_cntrl = DatabasePoolController(logger=logger)
    
    # BaseController.initialize(db=db_pool_cntrl.get_db(), logger=logger)
    
    # # db = db_pool_cntrl.get_db()
    
    book_service = BookService()
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    books_pb2_grpc.add_BookServiceServicer_to_server(book_service, server)
    
    server.add_insecure_port('[::]:50051')
    print("gRPC server running on port 50051...")
    
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()