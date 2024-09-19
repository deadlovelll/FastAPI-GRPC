from modules.base_controller import BaseController
from psycopg2 import DatabaseError, OperationalError, IntegrityError, InterfaceError, ProgrammingError, DataError
from fastapi.responses import JSONResponse

from controllers.jwt_security import JWTSecurity

import pika

class DeleteController(BaseController):
    
    def __init__(self) -> None:
        super().__init__()
        
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='book_queue')
        
    async def delete_book(self, book_id:int, token: str) -> JSONResponse:
        
        is_valid_token = await JWTSecurity.validate_jwt(token)
        
        if is_valid_token:
            
            try:
        
                message = f"Deleting Book|{book_id}"
                
                self.channel.basic_publish(exchange='', routing_key='book_queue', body=message)
                
                self.logger.info('task queued successfully')
                
                status = 'SUCCESS'
                
            finally:
                
                response = {'STATUS':status}
                
                return JSONResponse(response)
        
        else:
            
            return JSONResponse({'STATUS':'FAILED'})