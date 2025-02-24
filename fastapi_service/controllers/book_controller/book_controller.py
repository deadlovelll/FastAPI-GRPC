from fastapi.responses import JSONResponse  

from fastapi_service.controllers.rabbitmq_controller.rabbitmq_controller import RabbitMQController
from grpc_service.books_pb import books_pb2

from fastapi_service.modules.logger.logger import LoggerModule

class BookController:
    
    """
    Controller for managing book operations.

    This class provides methods for interacting with books via gRPC and 
    queues operations for book creation, deletion, and editing via RabbitMQ.
    """
    
    def __init__ (
        self, 
        grpc_stub, 
        logger: LoggerModule = LoggerModule(),
    ) -> None:
        
        """
        Initializes the BookController.

        :param grpc_stub: The gRPC stub used for communicating with the book service.
        :param logger: The logger instance for logging messages and errors.
        """
        
        self.grpc_stub = grpc_stub
        self.logger = logger.logger_initialization()
        self.rabbitmq_controller = RabbitMQController()

    async def get_all_books (
        self, 
    ) -> JSONResponse:
        
        """
        Retrieves all books from the book service.

        Publishes a message to RabbitMQ indicating that book retrieval is being performed.

        :return: JSONResponse containing a list of all books or an error message.
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
        Retrieves a book by its ID.

        Publishes a message to RabbitMQ indicating that a book retrieval is requested.

        :param book_id: The ID of the book to retrieve.
        :return: JSONResponse containing the book details or an error message.
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
        Queues an edit operation for a book.

        Publishes a message to RabbitMQ with the book edit request.

        :param book_id: The ID of the book to edit.
        :param book_name: The new name of the book.
        :param author: The new author of the book.
        :return: JSONResponse confirming that the edit request has been queued.
        """
        
        try:
            message = f"Editing Book|{book_id}|{book_name}|{author}"
            self.rabbitmq_controller.publish(message)
            
            self.logger.info (
                'Edit book task queued successfully for book_id: %s', 
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
        Queues a delete operation for a book.

        Publishes a message to RabbitMQ with the book deletion request.

        :param book_id: The ID of the book to delete.
        :return: JSONResponse confirming that the delete request has been queued.
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
        Queues a create operation for a new book.

        Publishes a message to RabbitMQ with the book creation request.

        :param book_name: The name of the new book.
        :param book_author: The author of the new book.
        :return: JSONResponse confirming that the create request has been queued.
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
