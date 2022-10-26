from flask import Blueprint, jsonify, abort, make_response
hello_world_bp = Blueprint("hello_world", __name__)

class Book:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description

books = [
        Book(1, "Book A", "Description A"),
        Book(2, "Book B", "Description B"),
        Book(3, "Book C", "Description C")
    ]

def validate_book(book_id):
    #handle invalid book_id
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message": f"book {book_id} is invalid"}, 400))

    #search  for book_id in data, return book
    for book in books:
        if book_id == book.id:
            return book
            
    #return a 404 for non-existing book
    abort(make_response({"message": f"book {book_id} not found"}, 404))

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("", methods=["GET"])
def handle_books():
    books_response = []
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description})
    return jsonify(books_response)

@books_bp.route("/<book_id>", methods = ["GET"])
def handle_book(book_id):
    book = validate_book(book_id)
    print(book)
    return {"id": book.id,
        "title": book.title,
        "description": book.description}
            
    #Add route and function to get a single book endpoint
    #Add response to handle book in books/<book_id> route
    #Add response to handle 400 for a invalid book_id in books/<book_id> route
    #Add response to handle 404 for a non-existing book in books/<book_id> route
 


@hello_world_bp.route("/hello-world", methods=["GET"])
def say_hello_world():
    my_beatiful_response_body = "Hello, World!"
    return my_beatiful_response_body, 200

@hello_world_bp.route("/hello/JSON", methods=["GET"])
def say_hello_json():
    my_beatiful_response_body = {
  "name": "Ada Lovelace",
  "message": "Hello!",
  "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
}
    return my_beatiful_response_body, 200

@hello_world_bp.route("/broken-endpoint-with-broken-server-code", methods=["GET"])
def broken_endpoint():
    response_body = {
  "name": "Ada Lovelace",
  "message": "Hello!",
  "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
}
    new_hobby = ["Surfing"]
    response_body["hobbies"].append(new_hobby)
    return response_body, 201


