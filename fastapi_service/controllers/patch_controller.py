from modules.base_controller import BaseController
from fastapi.responses import JSONResponse

from .jwt_security import JWTSecurity

import pika

class PatchController(BaseController):
    
    def __init__(self) -> None:
        super().__init__()
        
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='book_queue')
        
    async def editbook(self, book_id: int, book_name: str, author: str, token: str) -> JSONResponse:
        
        is_valid_token = await JWTSecurity.validate_jwt(token)
        
        if is_valid_token:
            
            try:
        
                message = f"Editing Book|{book_id}|{book_name}|{author}"
                
                self.channel.basic_publish(exchange='', routing_key='book_queue', body=message)
                
                self.logger.info('task queued successfully')
                
                status = 'SUCCESS'
                    
            except Exception as e:
                
                status = 'FAILED'
                
                self.logger.fatal('And exception occured', exc_info=True)
            
            finally:
                
                response = {'STATUS':status}
                    
                return JSONResponse(response)
            
        else:
            
            return JSONResponse({'STATUS':'FAILED'})