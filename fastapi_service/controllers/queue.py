import grpc
import logging

import books_pb2
import books_pb2_grpc

class BookQueueConsumer:
    def __init__(self, rabbit_client, grpc_host: str = 'localhost:50051', logger: logging.Logger = None) -> None:
        """
        Initialize the BookQueueConsumer.

        :param rabbit_client: An instance of RabbitMQClient (which provides a connection and channel).
        :param grpc_host: The gRPC host address.
        :param logger: Optional logger instance.
        """
        self.rabbit_client = rabbit_client
        self.grpc_host = grpc_host
        self.channel = self.rabbit_client.channel  # reuse the channel from the RabbitMQ client
        self.logger = logger or logging.getLogger(__name__)

    def process_message(self, message: str) -> None:
        """
        Parse the incoming message and dispatch the corresponding gRPC call.
        """
        parts = message.split('|')
        self.logger.info("Processing message parts: %s", parts)

        if parts[0] == 'Posting Book':
            self.logger.info("Processing 'Posting Book' request")
            with grpc.insecure_channel(self.grpc_host) as channel:
                stub = books_pb2_grpc.BookServiceStub(channel)
                request = books_pb2.PostBookRequest(book_name=parts[1], book_author=parts[2])
                response = stub.PostBook(request)
                self.logger.info("Book created: %s", response)

        elif parts[0] == 'Deleting Book':
            self.logger.info("Processing 'Deleting Book' request")
            with grpc.insecure_channel(self.grpc_host) as channel:
                stub = books_pb2_grpc.BookServiceStub(channel)
                request = books_pb2.DeleteBookRequest(book_id=int(parts[1]))
                response = stub.DeleteBook(request)
                self.logger.info("Book deleted: %s", response)

        elif parts[0] == 'Editing Book':
            self.logger.info("Processing 'Editing Book' request")
            with grpc.insecure_channel(self.grpc_host) as channel:
                stub = books_pb2_grpc.BookServiceStub(channel)
                request = books_pb2.UpdateBookRequest(
                    book_id=int(parts[1]),
                    book_name=parts[2],
                    author=parts[3]
                )
                response = stub.UpdateBook(request)
                self.logger.info("Book updated: %s", response)

        else:
            self.logger.warning("Unknown message type: %s", parts[0])

    def callback(self, ch, method, properties, body) -> None:
        """
        RabbitMQ callback method that decodes the message and processes it.
        """
        try:
            message = body.decode()
            self.logger.info("Received message: %s", message)
            self.process_message(message)
        except Exception as e:
            self.logger.error("Error processing message: %s", e, exc_info=True)

    def start_consuming(self) -> None:
        """
        Start consuming messages from the RabbitMQ queue.
        """
        self.channel.basic_consume(
            queue=self.rabbit_client.queue_name,
            on_message_callback=self.callback,
            auto_ack=True
        )
        self.logger.info("Started consuming messages from queue: %s", self.rabbit_client.queue_name)
        self.channel.start_consuming()


# Example usage:
if __name__ == '__main__':
    import logging
    from rabbitmq_client import RabbitMQClient  # assuming this class is defined in a separate module

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("BookQueueConsumer")

    # Create a RabbitMQ client instance.
    rabbit_client = RabbitMQClient(host='localhost', queue_name='book_queue')

    # Instantiate and start the consumer.
    consumer = BookQueueConsumer(rabbit_client=rabbit_client, grpc_host='localhost:50051', logger=logger)
    consumer.start_consuming()
