from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.responses import JSONResponse

from schemas.book.book import Book
from schemas.book_response.book_response import BookResponse
from schemas.books_response.books_response import BooksResponse
from controllers.book_controller.book_controller import BookController

class BookEndpoints:
    
    """
    Class-based endpoints for book operations.
    
    This class encapsulates all the routes related to books,
    creating an internal APIRouter with the necessary endpoints.
    """

    def __init__ (
        self,
    ) -> None:
        
        """
        Initialize the BookEndpoints and set up the router.
        """
        
        self.router = APIRouter(prefix="/books", tags=["Books"])
        self._setup_routes()
        
    def _setup_routes (
        self,
    ) -> None:
        
        """
        Registers API routes with the router using a loop to minimize repetition.
        """
        
        routes = [
            {
                "path": "/",
                "endpoint": self.get_all_books,
                "methods": ["GET"],
                "response_model": BooksResponse,
                "summary": "Get all books",
                "description": "Retrieve a list of all books in the database.",
            },
            {
                "path": "/{book_id}",
                "endpoint": self.get_book_by_id,
                "methods": ["GET"],
                "response_model": BookResponse,
                "summary": "Get book by ID",
            },
            {
                "path": "/",
                "endpoint": self.post_book,
                "methods": ["POST"],
                "response_model": BookResponse,
                "summary": "Create a book",
            },
            {
                "path": "/{book_id}",
                "endpoint": self.edit_book,
                "methods": ["PATCH"],
                "response_model": BookResponse,
                "summary": "Edit a book",
            },
            {
                "path": "/{book_id}",
                "endpoint": self.delete_book,
                "methods": ["DELETE"],
                "response_model": BookResponse,
                "summary": "Delete a book",
            },
        ]

        for route in routes:
            self.router.add_api_route(**route)

        
    async def get_all_books (
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

    async def get_book_by_id (
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

    async def post_book (
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

    async def edit_book (
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

    async def delete_book (
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
