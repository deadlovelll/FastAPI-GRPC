from fastapi_service.schemas.book.book import Book

class BookResponse(Book):
    
    """
    Response model for book-related API responses.

    This extends the `Book` model by adding an `id` field, which represents
    the unique identifier of the book in the database.

    Attributes:
        id (int): The unique identifier of the book.
    """

    id: int