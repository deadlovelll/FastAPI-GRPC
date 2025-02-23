import os

import pika

from fastapi_service.modules.logger.logger import LoggerModule

class RabbitMQController:
    
    """
    A simple client to manage RabbitMQ connections and message publishing.

    This class provides methods to establish a connection to a RabbitMQ broker, 
    declare a queue, publish messages, and gracefully close the connection.
    """

    def __init__ (
        self, 
        host: str = os.getenv('RABBITMQ_HOST'), 
        queue_name: str = os.getenv('RABBITMQ_QUEUE_NAME'),
        logger: LoggerModule = LoggerModule(),
    ) -> None:
        
        """
        Initializes the RabbitMQController.

        :param host: The hostname of the RabbitMQ server. Defaults to the environment variable 'RABBITMQ_HOST'.
        :param queue_name: The name of the queue to interact with. Defaults to the environment variable 'RABBITMQ_QUEUE_NAME'.
        """
        
        self.host = host
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.logger = logger
        self.connect()

    def connect (
        self,
    ) -> None:
        
        """
        Establishes a connection to RabbitMQ and declares the queue.

        This method attempts to connect to the RabbitMQ broker, open a communication channel, 
        and declare the specified queue to ensure it exists before messages are sent or received.
        """
        
        try:
            self.connection = pika.BlockingConnection (
                pika.ConnectionParameters (
                    host=self.host
                )
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name)
            
            self.logger.info (
                'Connected to RabbitMQ on host "%s" and declared queue "%s".', 
                self.host, 
                self.queue_name,
            )
            
        except Exception as e:
            
            self.logger.error (
                "Failed to connect to RabbitMQ: %s", 
                e, 
                exc_info=True,
            )
            
            self.connection = None
            self.channel = None

    def publish (
        self, 
        message: str, 
        exchange: str = '',
    ) -> None:
        
        """
        Publishes a message to the configured queue.

        :param message: The message to be sent to the queue.
        :param exchange: The exchange to publish to (default is the empty string for direct queue publishing).
        
        :raises Exception: If message publishing fails, an exception is logged and re-raised.
        """
        
        try:
            self.channel.basic_publish (
                exchange=exchange, 
                routing_key=self.queue_name, 
                body=message,
            )
            
            self.logger.info (
                'Message published to queue "%s": %s', 
                self.queue_name, 
                message,
            )
            
        except Exception as e:
            
            self.logger.error (
                'Failed to publish message: %s', 
                e, 
                exc_info=True,
            )
            
            raise

    def close (
        self,
    ) -> None:
        
        """
        Closes the connection to RabbitMQ.

        Ensures that the connection is properly closed to release resources and avoid memory leaks.
        """
        
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            self.logger.info("RabbitMQ connection closed.")
