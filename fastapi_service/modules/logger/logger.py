import os
import logging
import json
import socket
import logstash

from logging import Logger

class LoggerModule:
    
    """
    A class to initialize and configure a logger with Logstash integration.

    This module sets up a logger that sends structured logs to a Logstash server.
    """
    
    def __init__ (
        self,
    ) -> None:
        
        """
        Initializes the logger module by reading environment variables for Logstash configuration.
        """
        
        self.host = os.getenv('LOGGER_HOST')
        self.port = os.getenv('LOGGER_PORT')
        self.version = os.getenv('LOGGER_VERSION')
        
    def logger_initialization (
        self,
    ) -> Logger:
        
        """
        Initializes and configures the logger with a Logstash handler.

        The logger will send structured log messages in JSON format to a Logstash server.

        Returns:
            Logger: A configured logger instance.
        """
        
        logger = logging.getLogger('fastapi-logger')
        logger.setLevel(logging.INFO)

        class CustomLogstashFormatter(logging.Formatter):
            
            """
            Custom formatter for structuring log messages in JSON format.
            """
            
            def format (
                self, 
                record,
            ) -> bytes:
                
                """
                Formats log records into a structured JSON format.

                Args:
                    record (LogRecord): The log record to be formatted.

                Returns:
                    bytes: The formatted log message in JSON.
                """
                
                log_record = {
                    'message': record.getMessage(),
                    'level': record.levelname,
                    'timestamp': self.formatTime(record, self.datefmt),
                    'host': socket.gethostname(),
                    'method': record.funcName,  
                    'filename': record.filename,  
                    'line_number': record.lineno,
                }
                return json.dumps(log_record).encode('utf-8')  

        logstash_handler = logstash.LogstashHandler (
            host=self.host, 
            port=int(self.port),         
            version=int(self.version),
        )
        
        logstash_handler.setFormatter(CustomLogstashFormatter())
        logger.addHandler(logstash_handler)
        
        return logger
        
