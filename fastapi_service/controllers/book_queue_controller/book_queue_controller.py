from fastapi_service.modules.logger.logger import LoggerModule
from fastapi_service.controllers.book_controller.book_controller import BookController
from fastapi_service.controllers.rabbitmq_controller.rabbitmq_controller import RabbitMQController

class BookQueueConsumer:
    
    """
    RabbitMQ Consumer for processing book-related messages.

    This class listens to a RabbitMQ queue and processes incoming messages 
    related to book operations, such as creating, updating, or deleting books.
    """
    
    def __init__ (
        self, 
        rabbit_client: RabbitMQController = RabbitMQController(), 
        book_service: BookController = BookController(), 
        logger: LoggerModule = LoggerModule(),
    ) -> None:
        
        """
        Initializes the BookQueueConsumer.

        :param rabbit_client: An instance of RabbitMQController to handle messaging.
        :param book_service: An instance of BookController to perform book-related operations.
        :param logger: A logger instance for logging events.
        """
        
        self.rabbit_client = rabbit_client
        self.book_service = book_service
        self.logger = logger
        
        self.action_handlers = {
            "Posting Book": self._handle_create_book,
            "Deleting Book": self._handle_delete_book,
            "Editing Book": self._handle_update_book,
        }

    def process_message (
        self,
        message: str,
    ) -> None:
        
        """
        Parses and processes incoming messages from the queue.

        :param message: The raw message string received from RabbitMQ.
        """
        
        parts = message.split('|')
        action = parts[0]

        self.logger.info("Processing message: %s", message)

        try:
            parts = message.split('|')
            action = parts[0]

            handler = self.action_handlers.get(action)

            if handler:
                handler(parts)
            else:
                self.logger.warning (
                    'Unknown message type: %s', 
                    action,
                )

        except Exception as e:
            
            self.logger.error (
                'Error processing message: %s', 
                e, 
                exc_info=True,
            )
            
    def _handle_create_book (
        self, 
        parts: list,
    ) -> None:
        
        """
        Handles messages related to creating a new book.

        :param parts: A list of message components where:
                      - parts[1]: Book name
                      - parts[2]: Book author
        """
        
        if len(parts) < 3:
            self.logger.error (
                "Invalid message format for 'Posting Book': %s", 
                parts,
            )
            return
        
        book_name, book_author = parts[1], parts[2]
        self.book_service.create_book (
            book_name, 
            book_author,
        )

    def _handle_delete_book (
        self, 
        parts: list,
    ) -> None:
        
        """
        Handles messages related to deleting a book.

        :param parts: A list of message components where:
                      - parts[1]: Book ID
        """
        
        if len(parts) < 2:
            self.logger.error (
                "Invalid message format for 'Deleting Book': %s", 
                parts,
            )
            return
        
        book_id = int(parts[1])
        self.book_service.delete_book(book_id)

    def _handle_update_book (
        self, 
        parts: list
    ) -> None:
        
        """
        Handles messages related to updating an existing book.

        :param parts: A list of message components where:
                      - parts[1]: Book ID
                      - parts[2]: New book name
                      - parts[3]: New author
        """
        
        if len(parts) < 4:
            self.logger.error (
                'Invalid message format for "Editing Book": %s', 
                parts,
            )
            return

        book_id, book_name, author = int(parts[1]), parts[2], parts[3]
        self.book_service.update_book (
            book_id, 
            book_name, 
            author,
        )

    def callback (
        self, 
        ch, 
        method, 
        properties, 
        body,
    ) -> None:
        
        """
        RabbitMQ callback function for message consumption.

        This method is triggered when a message is received from RabbitMQ.

        :param ch: The channel object.
        :param method: The method frame with delivery information.
        :param properties: The properties of the received message.
        :param body: The message body received from RabbitMQ.
        """
        
        try:
            message = body.decode()
            self.process_message(message)
            
        except Exception as e:
            
            self.logger.error (
                "Error decoding message: %s", 
                e, 
                exc_info=True,
            )

    def start_consuming (
        self,
    ) -> None:
        
        """
        Starts the RabbitMQ consumer to listen for messages continuously.
        """
        
        self.rabbit_client.consume(self.callback)