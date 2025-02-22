import os

import pika
import logging

class RabbitMQController:
    
    """
    A simple client to manage RabbitMQ connections and message publishing.
    """

    def __init__ (
        self, 
        host: str = os.getenv('RABBITMQ_HOST'), 
        queue_name: str = os.getenv('RABBITMQ_QUEUE_NAME'),
    ) -> None:
        
        self.host = host
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.logger = logging.getLogger(__name__)
        self.connect()

    def connect (
        self,
    ) -> None:
        
        """
        Establish a connection to RabbitMQ and declare the queue.
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
        Publish a message to the configured queue.
        
        :param message: The message to be sent.
        :param exchange: The exchange to publish to (default is direct to the queue).
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
        Close the connection to RabbitMQ.
        """
        
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            self.logger.info("RabbitMQ connection closed.")
