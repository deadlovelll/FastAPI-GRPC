from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import grpc

from fastapi_service.modules.database.pool_controller.database_controller import DatabasePoolController
from fastapi_service.modules.database.model.database import Database
from fastapi_service.modules.logger.logger import LoggerModel
from modules.base_controller import BaseController

from controllers.get_controller import GetController
from controllers.post_controller import PostController
from controllers.delete_controller import DeleteController
from controllers.patch_controller import PatchController

from schemas.book.book import Book
from schemas.book_response.book_response import BookResponse
from schemas.books_response.books_response import BooksResponse

from pydantic import BaseModel

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
    return JSONResponse({'hello':'world!'})

@app.get (
    '/get-all-books', 
    response_model=BooksResponse, 
    summary="Get all books", 
    description="Retrieve a list of all books in the database."
)
async def get_all_books (
    token: str,
) -> JSONResponse:
    
    return await GetBookController.get_all_books (
        token,
    )

@app.post (
    '/post-book', 
    response_model=BookResponse,
)
async def post_book (
    book: Book, 
    token: str,
) -> JSONResponse:
    
    return await PostBookController.create_book (
        book.book_name, 
        book.book_author, 
        token
    )

@app.patch (
    '/edit-book', 
    response_model=BookResponse,
)
async def edit_book (
    book_id: int, 
    book: Book, 
    token: str
) -> JSONResponse:
    
    return await PatchBookController.editbook (
        book_id, 
        book.book_name, 
        book.book_author, 
        token,
    )

@app.get (
    '/get-all-books', 
    response_model=BooksResponse,
)
async def get_all_books (
    token: str,
) -> JSONResponse:
    
    return await GetBookController.get_all_books (
        token,
    )

@app.get (
    '/get-book-{book_id}', 
    response_model=BookResponse
)
async def get_book_by_id (
    book_id: int, 
    token: str,
) -> JSONResponse:
    
    return await GetBookController.get_book_by_id (
        book_id, 
        token,
    )

@app.delete (
    '/delete-book', 
    response_model=BookResponse,
)
async def delete_book (
    book_id: int, 
    token: str,
) -> JSONResponse:
    
    return await DeleteBookController.delete_book (
        book_id, 
        token,
    )

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8100)