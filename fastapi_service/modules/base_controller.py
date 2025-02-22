from .database.model.database import Database
from logging import Logger

class BaseController:
    db: Database = None  
    logger: Logger = None  

    def __init__(self) -> None:
        if not BaseController.db or not BaseController.logger:
            raise ValueError("BaseController requires 'db' and 'logger' to be set.")
    
    @classmethod
    def initialize(cls, db: Database, logger: Logger) -> None:
        cls.db = db
        cls.logger = logger
    