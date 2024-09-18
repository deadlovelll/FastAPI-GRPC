from ..modules.base_controller import BaseController
from psycopg2 import DatabaseError, OperationalError, IntegrityError, InterfaceError, ProgrammingError, DataError
from fastapi.responses import JSONResponse

from jwt_security import JWTSecurity


class GetController(BaseController):
    
    def __init__(self) -> None:
        super().__init__()
        
    async def get_all_books(self, token: str) -> JSONResponse:
        
        is_valid_token = await JWTSecurity.validate_jwt(token)
        
        if is_valid_token:
        
            try:
            
                connection = self.db.get_connection()
                cursor = connection.cursor()
                
                query = '''
                SELECT *
                FROM base_book
                '''
                
                cursor.execute(query)
                
                books = cursor.fetchall()
                
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
                
                if status == 'SUCCESS':
                    
                    response['BOOKS'] = books
                    
                return JSONResponse(response)
            
        else:
            
            return JSONResponse({'STATUS':'FAILED'})
    
    async def get_book_by_id(self, book_id: int, token: str) -> JSONResponse:
        
        is_valid_token = await JWTSecurity.validate_jwt(token)
        
        if is_valid_token:
        
            try:
                
                connection = self.db.get_connection()
                cursor = connection.cursor()
                
                query = '''
                SELECT *
                FROM base_book
                WHERE id = %s
                '''
                
                cursor.execute(query, str(book_id))
                book_details = cursor.fetchone()
                
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
                
                if status == 'SUCCESS':
                    
                    response['BOOK_DETAILS'] = book_details
                    
                return JSONResponse(response)
            
        else:
            
            return JSONResponse({'STATUS':'FAILED'})