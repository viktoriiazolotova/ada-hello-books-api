from app import db
from app.models.author import Author
from app.models.book import Book
from flask import abort, Blueprint, jsonify, make_response, request
from .book_routes import validate_model

authors_bp = Blueprint("authors_bp", __name__, url_prefix="/authors")

@authors_bp.route("", methods=['POST'])
def create_author():
    request_body = request.get_json()
    new_author = Author.from_dict(request_body)
    db.session.add(new_author) # tell db to add data to db
    db.session.commit()    # to committ changes

    return make_response(jsonify(f"Author {new_author.name} successfully created"), 201)

@authors_bp.route("", methods=["GET"])
def read_all_authors():
    name_query_value = request.args.get("name")

    
    if name_query_value:
       # method query is inherits from db.Model in Books class
        authors = Author.query.filter_by(name=name_query_value)
    else:
         authors = Author.query.all()
    
    authors_response = []
    
    for author in authors:
        authors_response.append(author.to_dict())
    return jsonify(authors_response)


@authors_bp.route("/<author_id>", methods = ["GET"])
def get_one_author(author_id):
    author = validate_model(Author, author_id)
    return author.to_dict()



from app.book_routes import validate_model

@authors_bp.route("/<author_id>/books", methods=["POST"])
def create_book(author_id):

    author = validate_model(Author, author_id)

    request_body = request.get_json()
    new_book = Book(
        title=request_body["title"],
        description=request_body["description"],
        author=author
    )
    db.session.add(new_book)
    db.session.commit()
    return make_response(jsonify(f"Book {new_book.title} by {new_book.author.name} successfully created"), 201)

@authors_bp.route("/<author_id>/books", methods=["GET"])
def read_books(author_id):
    author = validate_model(Author, author_id)

    books_response = []
    for book in author.books:
        books_response.append(
            {
            "id": book.id,
            "title": book.title,
            "description": book.description
            }
        )
    return jsonify(books_response)

