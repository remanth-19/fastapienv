from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status
app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=2)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(min_length=3)

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'Book Name',
                'author': 'Name of the author',
                'description': 'Give some context of the book',
                'rating': 5,
                'published_date': 2012
            }
        }



BOOKS = [
    Book(1,'Cracking the code interview','carol s dwek', 'this will help you to pass the interviews',3, 2012),
    Book(2, 'Mindset', 'dwek', 'growth mindset', 5,2012),
    Book(3, 'outliers', 'carol', 'helps you to become successful', 4,2013),
    Book(4, '5 Am club', 'robin sharma', 'early riser gets the worm', 4,2015),
    Book(5, 'Atomic habits', 'james clear', 'small changes will have big results', 5,2015)
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def get_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail=f"Book with the given {book_id} cannot be found")

#Using two queries in same path
@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_books_by_rating_or_published_date(rating: int = Query(None, gt=0, lt=6), published_date: int = Query(None, gt=2000, lt=2023)):
    return_books = []
    if published_date is None:
        for book in BOOKS:
            if book.rating == rating:
                return_books.append(book)
        return return_books
    elif rating is None:
        for book in BOOKS:
            if book.published_date == published_date:
                return_books.append(book)
        return return_books
    else:
        raise HTTPException(status_code=400, detail="Invalid query_param")
@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_req: BookRequest):
    new_book = Book(**book_req.model_dump())
    BOOKS.append(new_book)
    return BOOKS


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
