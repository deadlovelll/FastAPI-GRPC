from pydantic import BaseModel

class Book(BaseModel):
    
    """
    Data model representing a book.

    This model is used for validating and serializing book-related data in API requests and responses.

    Attributes:
        book_name (str): The name/title of the book.
        book_author (str): The author of the book.
    """
    
    book_name: str
    book_author: str