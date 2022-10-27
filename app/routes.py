from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("", methods=['POST'])
def create_book():
    request_body = request.get_json()
    new_book = Book(title=request_body["title"],
                    description=request_body["description"])
    db.session.add(new_book) # tell db to add data to db
    db.session.commit()    # to committ changes

    return make_response(f"Book {new_book.title} successfully created", 201)

@books_bp.route("", methods=["GET"])
def get_all_books():
    books_response = []
    books = Book.query.all()
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description})
    return jsonify(books_response)

# @books_bp.route("/<book_id>", methods = ["GET"])
# def handle_book(book_id):
#     book = validate_book(book_id)
#     print(book)
#     return {"id": book.id,
#         "title": book.title,
#         "description": book.description}

    #Add route and function to get a single book endpoint
    #Add response to handle book in books/<book_id> route
    #Add response to handle 400 for a invalid book_id in books/<book_id> route
    #Add response to handle 404 for a non-existing book in books/<book_id> route











