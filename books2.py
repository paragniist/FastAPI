from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status


app = FastAPI()


class Books:
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

BOOKS = [
    Books(1, 'Computer Science Pro', 'Author 5', 'A very nice book!', 5, 2030),
    Books(2, 'Be Fast with FastAPI', 'Author 6', 'A great book!', 5, 2030),
    Books(3, 'Master Endpoints', 'Author 7', 'A awesome book!', 5, 2029),
    Books(4, 'Gen AI-1', 'Author 1', 'Book Description', 2, 2028),
    Books(5, 'Gen AI-2', 'Author 2', 'Book Description', 3, 2027),
    Books(6, 'Gen AI-3', 'Author 3', 'Book Description', 1, 2026)
]


class Bookrequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=5)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2035)

    model_config = {
        'json_schema_extra': {
            "example": {
                "title": "Computer science python book",
                "author": "Coding Author",
                "description": "It is a knowledgable book",
                "rating": 4,
                "published_date": 2025
            }
        }
    }


@app.get("/books")
async def read_all_book():
    return BOOKS;


@app.get("/books/{book_id}")
async def read_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, details='Item not found')


@app.get("/books/")
async def read_by_ratings(book_rating: str = Query(gt=0, lt=6)):
    book_to_read = []
    for book in BOOKS:
        if book.rating == book_rating:
            book_to_read.append(book)
    return book_to_read


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def updating(book: Bookrequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')


@app.delete("/books/deleted_books", status_code=status.HTTP_204_NO_CONTENT)
async def deleting_book(book_id: int):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, details='Item not found')


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: Bookrequest):
      new_book = Books(**book_request.model_dump())
      BOOKS.append(find_book_id(new_book))


def find_book_id(book: Books):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
