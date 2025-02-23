from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.responses import JSONResponse

from schemas.book.book import Book
from schemas.book_response.book_response import BookResponse
from schemas.books_response.books_response import BooksResponse
from controllers.book_controller.book_controller import BookController

router = APIRouter (
    prefix='/books',
    tags=['Books'],
)

@router.get(
    '/',
    response_model=BooksResponse,
    summary='Get all books',
    description='Retrieve a list of all books in the database.'
)
async def get_all_books(
    token: str,
    controller: BookController = Depends(BookController)
) -> JSONResponse:
    
    return await controller.get_all_books (
        token,
    )

@router.get(
    "/{book_id}",
    response_model=BookResponse,
    summary="Get book by ID",
)
async def get_book_by_id(
    book_id: int,
    token: str,
    controller: BookController = Depends(BookController)
) -> JSONResponse:
    
    return await controller.get_book_by_id (
        book_id, 
        token,
    )

@router.post(
    "/",
    response_model=BookResponse,
    summary="Create a book",
)
async def post_book(
    book: Book,
    token: str,
    controller: BookController = Depends(BookController)
) -> JSONResponse:
    
    return await controller.create_book (
        book.book_name, 
        book.book_author, 
        token,
    )

@router.patch(
    "/{book_id}",
    response_model=BookResponse,
    summary="Edit a book",
)
async def edit_book(
    book_id: int,
    book: Book,
    token: str,
    controller: BookController = Depends(BookController)
) -> JSONResponse:
    
    return await controller.edit_book (
        book_id, 
        book.book_name, 
        book.book_author, 
        token,
    )

@router.delete(
    "/{book_id}",
    response_model=BookResponse,
    summary="Delete a book",
)
async def delete_book(
    book_id: int,
    token: str,
    controller: BookController = Depends(BookController)
) -> JSONResponse:
    
    return await controller.delete_book (
        book_id, 
        token,
    )
