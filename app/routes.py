from app import db 
from app.models.book import Book 
from flask import Blueprint, jsonify, make_response, request 

# Blueprint = Flask class that provides a pattern for grouping related routes 
# (endpoints).
# jsonify = Flask utility function that turns its argument into JSON. 

# syntax for instantiating a Blueprint instance 
# first arg = string used to identify this Blueprint
# second arg = almost always __name__ (which the blueprint uses to figure out 
# certain aspects of routing)
# Also, Blueprint provides an optional parameter url_prefix. 
# By setting the url_prefix value to "/books", all endpoints that use the 
# books_bp Blueprint will start with /books.
books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

@books_bp.route("", methods=["GET", "POST"])
def books():
    if request.method == "GET":
        title_from_url = request.args.get("title")
        if title_from_url: # If the user is asking for a specific title... 
            books = Book.query.filter_by(title=title_from_url)
        else: # Or, if the user just wants all books...
            books = Book.query.all()

        books_response = []
        for book in books:
            books_response.append(
                {
                    "id": book.id,
                    "title" : book.title,
                    "description" : book.description
                }
            )
        return jsonify(books_response), 200

    elif request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body:
            return make_response("Invalid request", 400)
        new_book = Book(title=request_body["title"], description=request_body["description"])

        db.session.add(new_book) # stage change 
        db.session.commit() # commit the change
        return f"Book {new_book.title} successfully created", 201

@books_bp.route("/<book_id>", methods=["GET", "PUT", "DELETE"])
def book(book_id): 
    book = Book.query.get(book_id)
    if book is None: # Guard clause that works with all three methods 
        return make_response("Book not found.", 404)

    if request.method == "GET":
        return {
                "id" : book.id,
                "title" : book.title,
                "description" : book.description
            }, 200 # 200 is optional 

    elif request.method == "PUT":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body:
            return {
                "Message": "Request requires both a title and description." }, 400
        book.title = request_body["title"]
        book.description = request_body["description"]

        # Save the update to the DB 
        db.session.commit()

        return {
                    "id" : book.id,
                    "title" : book.title,
                    "description" : book.description
                }, 200 # 200 is optional 
    
    elif request.method == "DELETE":
        db.session.delete(book)
        db.session.commit()
        return { "Message" : f"{book.title} has been deleted" }, 200 
        # For a successful delete, give a 200 (unless your body is empty, 
        # in which case, give a 204).

# Flask will automatically convert a dictionary into an HTTP response body,
# So if we're returning a dict, we don't need to call jsonify().


