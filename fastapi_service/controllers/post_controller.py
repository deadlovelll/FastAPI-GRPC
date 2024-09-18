from modules.base_controller import BaseController
from fastapi.responses import JSONResponse
from datetime import datetime
from psycopg2 import DatabaseError, OperationalError, IntegrityError, InterfaceError, ProgrammingError, DataError

from jwt_security import JWTSecurity

class PostController(BaseController):
    
    def __init__(self) -> None:
        super().__init__()
        
    async def create_book(self, book_name: str, book_author: str, token: str) -> JSONResponse:
        
        is_valid_token = await JWTSecurity.validate_jwt(token)
        
        if is_valid_token:
        
            try:
            
                connection = self.db.get_connection()
                cursor = connection.cursor()
                
                query = '''
                INSERT INTO base_book
                VALUES book_name, author, uploaded_at (%s, %s, %s)
                '''
                
                cursor.execute(query, (book_name, book_author, datetime.now()))
                
                connection.commit()
                
                status = 'SUCCESS'
            
            except (DatabaseError, OperationalError, IntegrityError, InterfaceError, ProgrammingError, DataError) as e:
                
                status = 'FAILED'
                
                if connection:
                
                    connection.rollback()
                
                self.logger.fatal(f'Database error occured: {e}. Full traceback below', exc_info=True)
        
            except Exception as e:
                
                status = 'FAILED'
                
                if connection:
                    
                    connection.rollback()
                    
                self.logger.error("An unexpected error occurred: %s", str(e), exc_info=True)
                
            finally:
                
                cursor.close()
                self.db.release_connection(connection)
                
                response = {'STATUS':status}
                    
                return JSONResponse(response)
        
        else:
            
            return JSONResponse({'STATUS':'FAILED'})