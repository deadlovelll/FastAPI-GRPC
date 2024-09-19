from modules.base_controller import BaseController
from psycopg2 import DatabaseError, OperationalError, IntegrityError, InterfaceError, ProgrammingError, DataError
from fastapi.responses import JSONResponse

from controllers.jwt_security import JWTSecurity

import grpc
import fastapi_service.grpc_service.books_pb2 as books_pb2
import fastapi_service.grpc_service.books_pb2_grpc as books_pb2_grpc

import pika

def get_grpc_stub():
    channel = grpc.insecure_channel('localhost:50051')
    return books_pb2_grpc.BookServiceStub(channel)

class GetController(BaseController):
    
    def __init__(self) -> None:
        super().__init__()
        
        self.grpc_stub = get_grpc_stub()
        
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='book_queue')
        
    async def get_all_books(self, token: str) -> JSONResponse:
        
        try:
        
            is_valid_token = await JWTSecurity.validate_jwt(token)
            
            if is_valid_token:
                
                request = books_pb2.EmptyRequest()
                
                self.channel.basic_publish(exchange='', routing_key='book_queue', body='Fetching all books')
            
                books = self.grpc_stub.GetAllBooks(request)
                    
                status = 'SUCCESS'
                
            else:
                
                return JSONResponse({'STATUS':'FAILED'})
            
        except Exception as e:
            
            status = 'FAILED'
            
            self.logger.fatal('And exception occured', exc_info=True)
        
        finally:
            
            response = {'STATUS':status}
            
            if status == 'SUCCESS':
                response['BOOKS'] = books
                
            return JSONResponse(response)
    
    async def get_book_by_id(self, book_id: int, token: str) -> JSONResponse:
        
        is_valid_token = await JWTSecurity.validate_jwt(token)
        
        if is_valid_token:
        
            try:
                
                request = books_pb2.EmptyRequest()
                
                self.channel.basic_publish(exchange='', routing_key='book_queue', body='Fetching Book by Id')
            
                book = self.grpc_stub.GetBookById(request)
                    
                status = 'SUCCESS'
                
            except Exception as e:
                
                status = 'FAILED'
                
                self.logger.fatal('And exception occured', exc_info=True)
            
            finally:
                
                response = {'STATUS':status}
                
                if status == 'SUCCESS':
                    response['BOOK'] = book
                    
                return JSONResponse(response)
            
        else:
            
            return JSONResponse({'STATUS':'FAILED'})