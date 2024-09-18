import os
from dotenv import load_dotenv

import logging 
import logging.handlers
import json
import socket
import logstash

load_dotenv()

from logging.handlers import TimedRotatingFileHandler

class LoggerModel:
    
    def __init__(self) -> None:
        
        self.host = os.getenv('LOGGER_HOST')
        self.port = os.getenv('LOGGER_PORT')
        self.version = os.getenv('LOGGER_VERSION')
        
    def logger_initialization(self):
        logger = logging.getLogger('fastapi-logger')
        logger.setLevel(logging.INFO)

        class CustomLogstashFormatter(logging.Formatter):
            
            def format(self, record):
                log_record = {
                    'message': record.getMessage(),
                    'level': record.levelname,
                    'timestamp': self.formatTime(record, self.datefmt),
                    'host': socket.gethostname(),
                    'method': record.funcName,  
                    'filename': record.filename,  
                    'line_number': record.lineno
                }
                return json.dumps(log_record).encode('utf-8')  

        logstash_handler = logstash.LogstashHandler(
            host=self.host, 
            port=int(self.port),         
            version=int(self.version)
        )
        
        logstash_handler.setFormatter(CustomLogstashFormatter())
        logger.addHandler(logstash_handler)
        
        return logger
        
