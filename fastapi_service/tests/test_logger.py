import unittest
import logging
import json
import socket
from unittest.mock import patch, MagicMock
from fastapi_service.modules.logger.logger import LoggerModule  

class TestLoggerModule(unittest.TestCase):
    
    @patch('fastapi_service.modules.logger.logger.load_dotenv')
    @patch('fastapi_service.modules.logger.logger.os.getenv')
    def test_logger_initialization(self, mock_getenv, mock_load_dotenv):
        """Тест инициализации логгера."""
        mock_getenv.side_effect = lambda key: {
            'LOGGER_HOST': 'localhost',
            'LOGGER_PORT': '5000',
            'LOGGER_VERSION': '1',
        }.get(key, '')

        logger_module = LoggerModule()
        logger = logger_module.logger_initialization()

        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, 'fastapi-logger')
        self.assertEqual(logger.level, logging.INFO)
        self.assertTrue(any(isinstance(h, logging.Handler) for h in logger.handlers))

    def test_custom_formatter(self):
        """Тест кастомного форматтера логов."""
        logger_module = LoggerModule()
        formatter = logger_module.logger_initialization().handlers[0].formatter
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="test_path",
            lineno=42,
            msg="Test log message",
            args=(),
            exc_info=None
        )
        formatted = formatter.format(record)
        log_dict = json.loads(formatted)

        self.assertEqual(log_dict["message"], "Test log message")
        self.assertEqual(log_dict["level"], "INFO")
        self.assertEqual(log_dict["line_number"], 42)
        self.assertEqual(log_dict["filename"], "test_path")
        self.assertEqual(log_dict["host"], socket.gethostname())

if __name__ == "__main__":
    unittest.main()
