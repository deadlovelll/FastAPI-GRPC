from typing import List

from pydantic import BaseModel

from schemas.book_response.book_response import BookResponse

class BooksResponse(BaseModel):
    books: List[BookResponse]