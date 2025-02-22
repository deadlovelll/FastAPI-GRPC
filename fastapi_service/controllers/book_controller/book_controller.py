import logging
from fastapi.responses import JSONResponse  
import books_pb2

from controllers.rabbitmq_controller.rabbitmq_controller import RabbitMQController

class BookController:
    
    def __init__ (
        self, 
        grpc_stub, 
        logger: logging.Logger,
    ) -> None:
        
        """
        Initialize the BookController with a gRPC stub and logger.
        Sets up a connection and channel to the RabbitMQ queue.
        """
        
        self.grpc_stub = grpc_stub
        self.logger = logger
        self.rabbitmq_controller = RabbitMQController()

    async def get_all_books (
        self, 
    ) -> JSONResponse:
        
        """
        Retrieve all books after validating the token.
        """
        
        try:
            request = books_pb2.EmptyRequest()
            self.rabbitmq_controller.publish('Fetching all books')
            books = self.grpc_stub.GetAllBooks(request)
            
            return JSONResponse (
                {
                    'STATUS': 'SUCCESS', 
                    'BOOKS': books,
                }, 
                status_code=200,
            )
        
        except Exception as e:
            
            self.logger.fatal (
                'Exception in get_all_books: %s', 
                str(e), 
                exc_info=True,
            )
            
            return JSONResponse (
                {
                    'STATUS': 'FAILED', 
                    'DETAIL': str(e),
                }, 
                status_code=500,
            )

    async def get_book_by_id (
        self, 
        book_id: int, 
    ) -> JSONResponse:
        
        """
        Retrieve a specific book by ID after token validation.
        """
        
        try:
            request = books_pb2.GetBookByIdRequest(book_id=book_id)
            self.rabbitmq_controller.publish(f'Fetching book by id: {book_id}')
            
            book = self.grpc_stub.GetBookById(request)
            
            return JSONResponse (
                {
                    'STATUS': 'SUCCESS', 
                    'BOOK': book,
                }, 
                status_code=200,
            )
        
        except Exception as e:
            
            self.logger.fatal (
                "Exception in get_book_by_id: %s", 
                str(e), 
                exc_info=True,
            )
            
            return JSONResponse (
                {
                    'STATUS': 'FAILED', 
                    'DETAIL': str(e),
                }, 
                status_code=500,
            )

    async def edit_book (
        self, 
        book_id: int, 
        book_name: str, 
        author: str, 
    ) -> JSONResponse:
        
        """
        Queue an edit operation for a book.
        """
        
        try:
            message = f"Editing Book|{book_id}|{book_name}|{author}"
            self.rabbitmq_controller.publish(message)
            
            self.logger.info (
                'Edit book task queued successfully for book_id: %s', 
                book_id
            
            )
            return JSONResponse (
                {
                    'STATUS': 'SUCCESS'
                }, 
                status_code=200,
            )
        
        except Exception as e:
            
            self.logger.fatal (
                'Exception in edit_book: %s', 
                str(e), 
                exc_info=True,
            )
            
            return JSONResponse (
                {
                    'STATUS': 'FAILED', 
                    'DETAIL': str(e),
                }, 
                status_code=500,
            )

    async def delete_book (
        self, 
        book_id: int, 
    ) -> JSONResponse:
        
        """
        Queue a delete operation for a book.
        """
        
        try:
            message = f"Deleting Book|{book_id}"
            self.rabbitmq_controller.publish(message)
            
            self.logger.info (
                'Delete book task queued successfully for book_id: %s', 
                book_id,
            )
            
            return JSONResponse (
                {
                    'STATUS': 'SUCCESS',
                }, 
                status_code=200,
            )
        
        except Exception as e:
            
            self.logger.fatal (
                "Exception in delete_book: %s", 
                str(e),
                exc_info=True,
            )
            
            return JSONResponse (
                {
                    'STATUS': 'FAILED', 
                    'DETAIL': str(e),
                }, 
                status_code=500,
            )

    async def create_book (
        self, 
        book_name: str, 
        book_author: str, 
    ) -> JSONResponse:
        
        """
        Queue a create operation for a new book.
        """
        
        try:
            message = f"Posting Book|{book_name}|{book_author}"
            self.rabbitmq_controller.publish(message)
            
            self.logger.info (
                'Create book task queued successfully for book: %s', 
                book_name,
            )
            
            return JSONResponse (
                {
                    'STATUS': 'SUCCESS',
                }, 
                status_code=201,
            )
        
        except Exception as e:
            
            self.logger.fatal (
                'Exception in create_book: %s', 
                str(e), 
                exc_info=True,
            )
            
            return JSONResponse (
                {
                    'STATUS': 'FAILED', 
                    'DETAIL': str(e),
                }, 
                status_code=500,
            )
