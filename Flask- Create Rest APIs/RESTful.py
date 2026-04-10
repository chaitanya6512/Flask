from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)

api = Api(app)

# Sample data
books = [
    {"id": 1, "title": "Concept of Physics", "author": "H.C Verma"},
    {"id": 2, "title": "Gunahon ka Devta", "author": "Dharamvir Bharti"},
    {"id": 3, "title": "Problems in General Physics", "author": "I.E Irodov"}
]

# API Resource class
class BookResource(Resource):
    def get(self, book_id=None):
        if book_id is None:
            return books, 200       # Explicitly return status 200
        book = next((book for book in books if book["id"] == book_id ), None)
        if book:
            return book, 200
        return {"error":"Book not Found!"}, 400     # Return 404 only when not found

    def post(self):
        new_book = request.json 
        books.append(new_book)
        return new_book, 201    # Created Status
    
    def put(self, book_id):
        book = next((book for book in books if book["id"] == book_id), None)
        if not book:
            return {"error":"Book not found"}, 404      # Explicit 404
        data = request.json
        book.update(data)
        return book, 200        # Return updated book with 200 ok
    
    def delete(self, book_id):
        global books
        books = [book for book in books if book["id"] != book_id]
        return {"message":"Book Deleted"}, 200
    
# Adding Resources to API
api.add_resource(BookResource,'/books','/books/<int:book_id>')

if __name__ == "__main__":
    app.run(debug=True)
