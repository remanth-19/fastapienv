from fastapi import FastAPI, Body

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

BOOKS = [
    Book(1,'Cracking the code interview','carol s dwek', 'this will help you to pass the interviews',4),
    Book(2, 'Mindset', 'dwek', 'growth mindset', 4),
    Book(3, 'outliers', 'carol', 'helps you to become successful', 4),
    Book(4, '5 Am club', 'robin sharma', 'early riser gets the worm', 4),
    Book(5, 'Atomic habits', 'james clear', 'small changes will have big results', 4)
]

@app.get("/books")
async def get_all_books():
    return BOOKS

@app.post("/create-book")
async def create_book(book_req = Body()):
    BOOKS.append(book_req)
    return BOOKS
