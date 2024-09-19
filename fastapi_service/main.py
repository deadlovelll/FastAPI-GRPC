from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import grpc

from modules.database_controller import DatabasePoolController
from modules.database import Database
from modules.logger import LoggerModel
from modules.base_controller import BaseController

from controllers.get_controller import GetController
from controllers.post_controller import PostController
from controllers.delete_controller import DeleteController
from controllers.patch_controller import PatchController

Logger = LoggerModel()
logger = Logger.logger_initialization()

PoolController = DatabasePoolController(logger=logger)

BaseController.initialize(db=PoolController.get_db(), logger=logger)

GetBookController = GetController()
PostBookController = PostController()
PatchBookController = PatchController()
DeleteBookController = DeleteController()

app = FastAPI()

@app.on_event('startup')
async def startup_event():
    
   await PoolController.startup_event()
    
@app.on_event('shutdown')
async def shutdown_event():
    
    await PoolController.shutdown_event()

@app.get('/')
async def initial_func():
    pass

@app.get('/get-all-books')
async def get_all_books(token: str) -> JSONResponse:
    
    return await GetBookController.get_all_books(token)

@app.get('/get-book-{book_id}')
async def get_book_by_id(book_id: int, token: str) -> JSONResponse:
    
    return await GetBookController.get_book_by_id(book_id, token)

@app.post('/post-book')
async def post_book(book_name: str, book_author: str, token: str) -> JSONResponse:
    
    return await PostBookController.post_book(book_name, book_author, token)

@app.patch('/edit-book')
async def edit_book(to_edit: dict, token: str) -> JSONResponse:
    
    return await PatchBookController.edit_book(to_edit, token)

@app.delete('/delete-book')
async def delete_book(book_id: int, token: str) -> JSONResponse:
    
    return await DeleteBookController.delete_book(book_id, token)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8100)