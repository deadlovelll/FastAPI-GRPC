from fastapi import FastAPI
import uvicorn

from modules.database_controller import DatabasePoolController
from modules.database import Database
from modules.logger import LoggerModel
from modules.base_controller import BaseController

Logger = LoggerModel()
logger = Logger.logger_initialization()

PoolController = DatabasePoolController(logger=logger)

BaseController.initialize(db=PoolController.get_db(), logger=logger)

app = FastAPI()

@app.on_event('startup')
async def startup_event():
    
   await PoolController.startup_event()
    
@app.on_event('shutdown')
async def shutdown_event():
    
    await PoolController.shutdown_event()

@app.get('/')
async def initial_funct():
    pass

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8100)