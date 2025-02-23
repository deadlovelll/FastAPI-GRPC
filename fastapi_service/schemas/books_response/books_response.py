from typing import List
from pydantic import BaseModel
from schemas.book_response.book_response import BookResponse

class BooksResponse(BaseModel):
    
    """
    Response model for a list of books.

    This model is used for serializing a list of book responses in API responses.

    Attributes:
        books (List[BookResponse]): A list of books with their details, including their ID, name, and author.
    """

    books: List[BookResponse]
