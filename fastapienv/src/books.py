from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

@app.get("/books")
async def read_all_books():
    return BOOKS

# path parameter
@app.get("/books/{book_title}")
async def read_book(book_title : str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

# Query parameter
@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

# An Example of both path and query parameters
@app.get("/books/{author}/")
async def read_books_by_author_category(author: str , category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold()  and \
            book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

# POST request example
@app.post("/books/create_book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)

# PUT req example
@app.post("/books/update_book")
async def update_books(update_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == update_book.get('title').casefold():
            BOOKS[i] = update_book

# Delete req example
@app.delete("/books/delete_book/{book_title}")
async def deleted_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break

# Get all books from a specified author
@app.get("/books/author/{author_name}")
async def get_books_by_authorName(author_name:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author_name.casefold():
            books_to_return.append(book)
    return books_to_return