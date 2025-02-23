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
    controller: BookController = Depends(BookController),
) -> JSONResponse:
    
    """
    Retrieve all books.

    Args:
        token (str): Authentication token extracted from the request header.
        controller (BookController): The controller responsible for book operations.

    Returns:
        JSONResponse: A response containing the list of books.
    """
    
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
    controller: BookController = Depends(BookController),
) -> JSONResponse:
    
    """
    Retrieve a single book by its ID.

    Args:
        book_id (int): The ID of the book to retrieve.
        token (str): Authentication token.
        controller (BookController): The controller responsible for book operations.

    Returns:
        JSONResponse: A response containing the requested book.
    """
    
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
    controller: BookController = Depends(BookController),
) -> JSONResponse:
    
    """
    Create a new book entry.

    Args:
        book (Book): The book data from the request body.
        token (str): Authentication token.
        controller (BookController): The controller responsible for book operations.

    Returns:
        JSONResponse: A response containing the created book.
    """
    
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
    controller: BookController = Depends(BookController),
) -> JSONResponse:
    
    """
    Update an existing book's details.

    Args:
        book_id (int): The ID of the book to update.
        book (Book): The updated book data.
        token (str): Authentication token.
        controller (BookController): The controller responsible for book operations.

    Returns:
        JSONResponse: A response containing the updated book.
    """
    
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
    controller: BookController = Depends(BookController),
) -> JSONResponse:
    
    """
    Delete a book by its ID.

    Args:
        book_id (int): The ID of the book to delete.
        token (str): Authentication token.
        controller (BookController): The controller responsible for book operations.

    Returns:
        JSONResponse: A response indicating the result of the delete operation.
    """
    
    return await controller.delete_book (
        book_id, 
        token,
    )
