from app import db
from app.models.book import Book
from flask import abort, Blueprint, jsonify, make_response, request

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

#helper functions
def validate_model(cls, model_id):
    #handle invalid model_id
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))
    #search for model_id in database, return model
    model = cls.query.get(model_id) # return None if no model
    
    #return 404 for non-existing model
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))
    return model

#route functions

@books_bp.route("", methods=['POST'])
def create_book():
    request_body = request.get_json()
    new_book = Book.from_dict(request_body)
    db.session.add(new_book) # tell db to add data to db
    db.session.commit()    # to committ changes

    return make_response(jsonify(f"Book {new_book.title} successfully created"), 201)

@books_bp.route("", methods=["GET"])
def read_all_books():
    title_query = request.args.get("title")

    
    if title_query:
       # method query is inherits from db.Model in Books class
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()
    
    books_response = []
    
    for book in books:
        books_response.append(book.to_dict())
    return jsonify(books_response)


@books_bp.route("/<book_id>", methods = ["GET"])
def read_one_book(book_id):
    book = validate_model(Book,book_id)
    return book.to_dict()

@books_bp.route("/<book_id>", methods = ["PUT"])
def update_book(book_id):
    book = validate_model(Book,book_id)
    
    request_body = request.get_json()
    list_keys = ["title", "description"]
    str_resp = ""
    try:
        book.title = request_body["title"]
        book.description = request_body["description"] ###### ask how to handle it
    except KeyError:
        for key in list_keys:
            if key not in request_body:
                str_resp += key + " "
        
        return make_response(f"Book #{book_id} missing {str_resp.strip()}", 200)
    db.session.commit()
    return make_response(jsonify(f"Book #{book_id} successfully updated"), 200)

@books_bp.route("/<book_id>", methods = ["DELETE"])   
def delete_book(book_id):
        book = validate_model(Book, book_id)
        db.session.delete(book)
        db.session.commit()
        return make_response(jsonify(f"Book #{book_id} successfully deleted"), 200)

    
    
    #Add route and function to get a single book endpoint
    #Add response to handle book in books/<book_id> route
    #Add response to handle 400 for a invalid book_id in books/<book_id> route
    #Add response to handle 404 for a non-existing book in books/<book_id> route











