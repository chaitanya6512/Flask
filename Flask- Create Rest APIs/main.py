from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data
books = [
    {"id": 1, "title": "Concept of Physics", "author": "H.C Verma"},
    {"id": 2, "title": "Gunahon ka Devta", "author": "Dharamvir Bharti"},
    {"id": 3, "title": "Problems in General Physsics", "author": "I.E Irodov"}
]

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

# Get a single book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    return jsonify(book) if book else (jsonify({'error': "Book not found"}), 404)

# Add a new book
@app.route('/books', methods=['POST'])
def add_book():
    new_book = request.json
    books.append(new_book)
    return jsonify(new_book), 201

# Update a book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if not book:
        return jsonify({'error':"Book not found"}), 404
    data = request.json
    book.update(data)
    return jsonify(book)
# Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [book for book in books if book['id'] != book_id]
    return jsonify({'message':"Book deleted"})


if __name__ == "__main__":
    app.run(debug=True)


# Explanation of Routes:
# GET/books : This route retrives all books from our dataset and returns them in JSON format.
# GET/books/<book_id> : This retrives a single book based on its ID. If the book is not found, it returns a 404 error.
# POST/books : This allows users to add a new book to the dataset by sending a JSON payload containing the book details.
# PUT/books/<book_id> : This updates an existing book's details based on the provided book ID. If the book is not found, it returns an error.
# DELETE/books/<book_id> : This removes a book from the dataset based on the book ID and returns a confirmation message.
