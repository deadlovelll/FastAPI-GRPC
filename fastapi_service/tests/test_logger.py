import unittest
import logging
import json
import socket
from unittest.mock import patch, MagicMock
from fastapi_service.modules.logger.logger import LoggerModule  

class TestLoggerModule(unittest.TestCase):
    
    """
    Unit tests for the LoggerModule class.

    This test suite ensures that:
    - The logger is initialized correctly with the expected configuration.
    - The custom log formatter produces correctly structured JSON log messages.
    """
    
    @patch('fastapi_service.modules.logger.logger.load_dotenv')
    @patch('fastapi_service.modules.logger.logger.os.getenv')
    def test_logger_initialization (
        self, 
        mock_getenv, 
        mock_load_dotenv,
    ) -> None:
        
        """
        Test the logger initialization process.

        This test verifies that:
        - The logger is an instance of `logging.Logger`.
        - The logger has the expected name (`fastapi-logger`).
        - The logger's log level is set to `INFO`.
        - The logger has at least one handler attached.

        Mocks:
        - `os.getenv`: Simulates environment variables for the logger configuration.
        - `load_dotenv`: Prevents actual environment variable loading.
        """
        
        mock_getenv.side_effect = lambda key: {
            'LOGGER_HOST': 'localhost',
            'LOGGER_PORT': '5000',
            'LOGGER_VERSION': '1',
        }.get(key, '')

        logger_module = LoggerModule()
        logger = logger_module.logger_initialization()

        self.assertIsInstance (
            logger, 
            logging.Logger,
        )
        self.assertEqual (
            logger.name, 
            'fastapi-logger',
        )
        self.assertEqual (
            logger.level, 
            logging.INFO,
        )
        self.assertTrue(any(isinstance(h, logging.Handler) for h in logger.handlers))

    def test_custom_formatter (
        self,
    ) -> None:
        
        """
        Test the custom log formatter.

        This test ensures that:
        - The formatter correctly formats log messages as JSON.
        - The JSON output contains the expected fields: `message`, `level`, 
          `line_number`, `filename`, and `host`.
        - The values in the formatted log match the log record.

        It creates a log record manually, applies the formatter, and then 
        verifies the parsed JSON structure.
        """
        
        logger_module = LoggerModule()
        formatter = logger_module.logger_initialization().handlers[0].formatter
        record = logging.LogRecord (
            name="test_logger",
            level=logging.INFO,
            pathname="test_path",
            lineno=42,
            msg="Test log message",
            args=(),
            exc_info=None,
        )
        formatted = formatter.format(record)
        log_dict = json.loads(formatted)

        self.assertEqual (
            log_dict["message"], 
            "Test log message",
        )
        self.assertEqual (
            log_dict["level"], 
            "INFO",
        )
        self.assertEqual (
            log_dict["line_number"], 
            42,
        )
        self.assertEqual (
            log_dict["filename"], 
            "test_path",
        )
        self.assertEqual (
            log_dict["host"], 
            socket.gethostname(),
        )

if __name__ == "__main__":
    unittest.main()
