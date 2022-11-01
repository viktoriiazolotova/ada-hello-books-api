from app import db
from app.models.book import Book
from flask import abort, Blueprint, jsonify, make_response, request

books_bp = Blueprint("books", __name__, url_prefix="/books")

#helper functions
def validate_book(book_id):
    #handle invalid book_id
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message": f"book {book_id} is invalid"}, 400))
    #search for book_id in database, return book

    book = Book.query.get(book_id) # return None if no book
    
    #return 404 for non-existing book
    if not book:
        abort(make_response({"message": f"book {book_id} is not found"}, 404))
    return book


#route functions
@books_bp.route("", methods=['POST'])
def create_book():
    request_body = request.get_json()
    new_book = Book(title=request_body["title"],
                    description=request_body["description"])
    db.session.add(new_book) # tell db to add data to db
    db.session.commit()    # to committ changes

    return make_response(f"Book {new_book.title} successfully created", 201)

@books_bp.route("", methods=["GET"])
def read_all_books():
    title_query = request.args.get("title")

    
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()
      
    
    books_response = []
    
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description})
    return jsonify(books_response)


@books_bp.route("/<book_id>", methods = ["GET"])
def read_one_book(book_id):
    book = validate_book(book_id)
    return {"id": book.id,
        "title": book.title,
        "description": book.description}

@books_bp.route("/<book_id>", methods = ["PUT"])
def update_book(book_id):
    book = validate_book(book_id)
    
    request_body = request.get_json()
    try:
        book.title = request_body["title"]
        book.description = request_body["description"] ###### ask how to handle it
    except KeyError:
        return make_response(f"Book #{book_id} missing data", 200)
    db.session.commit()
    return make_response(f"Book #{book_id} successfully updated", 200)

@books_bp.route("/<book_id>", methods = ["DELETE"])   
def delete_book(book_id):
        book = validate_book(book_id)
        db.session.delete(book)
        db.session.commit()

        return make_response(f"Book #{book_id} successfully deleted")

    
    
    #Add route and function to get a single book endpoint
    #Add response to handle book in books/<book_id> route
    #Add response to handle 400 for a invalid book_id in books/<book_id> route
    #Add response to handle 404 for a non-existing book in books/<book_id> route











