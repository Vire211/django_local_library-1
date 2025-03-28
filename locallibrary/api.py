import uuid
from ninja import NinjaAPI, Schema

api = NinjaAPI()

class HelloSchema(Schema):
    name: str = "world"

@api.post("/hello")
def hello(request, data: HelloSchema):
    return f"Hello {data.name}"

class UserSchema(Schema):
    username: str
    email: str
    first_name: str
    last_name: str

class Error(Schema):
    message: str

@api.get("/me", response={200: UserSchema, 403: Error})
def me(request):
    if not request.user.is_authenticated:
        return 403, {"message": "Please sign in first"}
    return request.user 

# Import the models
from catalog.models import Author, Genre, Book, BookInstance, Language
from django.shortcuts import get_object_or_404
from typing import List
from datetime import date
from typing import Optional

# CRUD classes for Genre
class GenreIn(Schema):
    name: str

class GenreOut(Schema):
    id: int
    name: str

# CRUD classes for Author
class AuthorIn(Schema):
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    date_of_death: Optional[date] = None

class AuthorOut(Schema):
    id: int
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    date_of_death: Optional[date] = None

# CRUD classes for Language
class LanguageIn(Schema):
    name: str

class LanguageOut(Schema):
    id: int
    name: str

# CRUD classes for Book
class BookIn(Schema):
    title: str
    author: AuthorIn
    summary: str
    isbn: str
    genre: GenreIn
    language: LanguageIn

class BookOut(Schema):
    id: int
    title: str
    author: AuthorOut
    summary: str
    isbn: str
    genre: List[GenreOut]
    language: LanguageOut

# CRUD classes for BookInstance
class BookInstanceIn(Schema):
    book: BookOut
    imprint: str
    due_back: Optional[date] = None
    status: str

class BookInstanceOut(Schema):
    book: BookOut
    imprint: str
    due_back: Optional[date] = None
    status: str

# Make every method have authentication except read
from ninja.security import HttpBearer

class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token

api = NinjaAPI(auth=GlobalAuth())

# Create
@api.post("/genres")
def create_genre(request, payload: GenreIn):
    genre = Genre.objects.create(**payload.dict())
    return {"id": genre.id}

@api.post("/authors")
def create_author(request, payload: AuthorIn):
    author = Author.objects.create(**payload.dict())
    return {"id": author.id}

@api.post("/languagess")
def create_language(request, payload: LanguageIn):
    language = Language.objects.create(**payload.dict())
    return {"id": language.id}

@api.post("/books")
def create_book(request, payload: BookIn):
    book = Book.objects.create(**payload.dict())
    return {"id": book.id}

@api.post("/bookinstances")
def create_bookInstance(request, payload: BookInstanceIn):
    book = BookInstance.objects.create(**payload.dict())
    return {"book": book.book}

# Retrieve
@api.get("/genres/{genre_id}", response=GenreOut, auth=None)
def get_genre(request, genre_id: int):
    genre = get_object_or_404(Genre, id=genre_id)
    return genre

@api.get("/genres", response=List[GenreOut], auth=None)
def list_genres(request):
    qs = Genre.objects.all()
    return qs

@api.get("/authors/{author_id}", response=AuthorOut, auth=None)
def get_author(request, author_id: int):
    author = get_object_or_404(Author, id=author_id)
    return author

@api.get("/authors", response=List[AuthorOut], auth=None)
def list_authors(request):
    qs = Author.objects.all()
    return qs

@api.get("/languages/{language_id}", response=LanguageOut, auth=None)
def get_language(request, language_id: int):
    language = get_object_or_404(Language, id=language_id)
    return language

@api.get("/languages", response=List[LanguageOut], auth=None)
def list_languages(request):
    qs = Language.objects.all()
    return qs

@api.get("/books/{book_id}", response=BookOut, auth=None)
def get_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    return book

@api.get("/books", response=List[BookOut], auth=None)
def list_books(request):
    qs = Book.objects.select_related("author")
    return list(qs)

@api.get("/bookinstances/{book_name}", response=List[BookInstanceOut], auth=None)
def get_bookinstance(request, book_name: str):
    books = BookInstance.objects.all()
    l = books.filter(book__title=book_name)
    return list(l)

# Update
@api.put("/genres/{genre_id}")
def update_genre(request, genre_id: int, payload: GenreIn):
    genre = get_object_or_404(Genre, id=genre_id)
    for attr, value in payload.dict().items():
        setattr(genre, attr, value)
    genre.save()
    return {"success": True}

@api.put("/languages/{language_id}")
def update_language(request, language_id: int, payload: LanguageIn):
    language = get_object_or_404(Language, id=language_id)
    for attr, value in payload.dict().items():
        setattr(language, attr, value)
    language.save()
    return {"success": True}

@api.put("/authors/{author_id}")
def update_author(request, author_id: int, payload: AuthorIn):
    author = get_object_or_404(Author, id=author_id)
    for attr, value in payload.dict().items():
        setattr(author, attr, value)
    author.save()
    return {"success": True}

@api.put("/books/{book_id}")
def update_book(request, book_id: int, payload: BookIn):
    book = get_object_or_404(Book, id=book_id)
    for attr, value in payload.dict().items():
        setattr(book, attr, value)
    book.save()
    return {"success": True}

@api.put("/bookinstances/{book_id}")
def update_bookInstance(request, book_id: str, payload: BookInstanceIn):
    book = get_object_or_404(BookInstance, id=book_id)
    for attr, value in payload.dict().items():
        setattr(book, attr, value)
    book.save()
    return {"success": True}

# Delete
@api.delete("/genres/{genre_id}")
def delete_genre(request, genre_id: int):
    genre = get_object_or_404(Genre, id=genre_id)
    genre.delete()
    return {"success": True}

@api.delete("/authors/{author_id}")
def delete_author(request, author_id: int):
    author = get_object_or_404(Author, id=author_id)
    author.delete()
    return {"success": True}

@api.delete("/languages/{language_id}")
def delete_language(request, language_id: int):
    language = get_object_or_404(Language, id=language_id)
    language.delete()
    return {"success": True}

@api.delete("/books/{book_id}")
def delete_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return {"success": True}

@api.delete("/books/{book_id}")
def delete_bookInstance(request, book_id: str):
    book = get_object_or_404(BookInstance, id=book_id)
    book.delete()
    return {"success": True}