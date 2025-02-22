import logging

class BookQueueConsumer:
    
    def __init__ (
        self, 
        rabbit_client, 
        book_service, 
        logger: logging.Logger = None,
    ) -> None:
        
        """
        RabbitMQ Consumer for processing book-related messages.
        """
        
        self.rabbit_client = rabbit_client
        self.book_service = book_service
        self.logger = logger or logging.getLogger(__name__)

    def process_message (
        self,
        message: str,
    ) -> None:
        
        """
        Parses and processes incoming messages.
        """
        
        parts = message.split('|')
        action = parts[0]

        self.logger.info("Processing message: %s", message)

        try:
            if action == 'Posting Book':
                book_name, book_author = parts[1], parts[2]
                self.book_service.create_book(book_name, book_author)

            elif action == 'Deleting Book':
                book_id = int(parts[1])
                self.book_service.delete_book(book_id)

            elif action == 'Editing Book':
                book_id, book_name, author = int(parts[1]), parts[2], parts[3]
                self.book_service.update_book(book_id, book_name, author)

            else:
                self.logger.warning("Unknown message type: %s", action)

        except Exception as e:
            self.logger.error("Error processing message: %s", e, exc_info=True)

    def callback (
        self, 
        ch, 
        method, 
        properties, 
        body,
    ) -> None:
        
        """
        RabbitMQ callback function.
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
        Starts the RabbitMQ consumer.
        """
        
        self.rabbit_client.consume(self.callback)