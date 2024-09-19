from modules.base_controller import BaseController
from fastapi.responses import JSONResponse
from datetime import datetime
from psycopg2 import DatabaseError, OperationalError, IntegrityError, InterfaceError, ProgrammingError, DataError

from controllers.jwt_security import JWTSecurity

import grpc
import books_pb2
import books_pb2_grpc as books_pb2_grpc

import pika
import json

class PostController(BaseController):
    
    def __init__(self) -> None:
        super().__init__()
        
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='book_queue')
        
    async def create_book(self, book_name: str, book_author: str, token: str) -> JSONResponse:
        
        is_valid_token = await JWTSecurity.validate_jwt(token)
        
        if is_valid_token:
            
            try:
            
                message = f"Posting Book|{book_name}|{book_author}"
                
                self.channel.basic_publish(exchange='', routing_key='book_queue', body=message)
                
                self.logger.info('task queued successfully')
                
                status = 'SUCCESS'
                
            except Exception as e:
                
                status = 'FAILED'
                
                self.logger.fatal('Unexpected error occured', exc_info=True)
                
            finally:
                
                response = {'STATUS':status}
                
                return JSONResponse(response)
        
        else:
            
            return JSONResponse({'STATUS':'FAILED'})