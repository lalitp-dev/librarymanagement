from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Update 'your_username' and 'your_password' with your PostgreSQL credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:lalit1@localhost/library_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    is_borrowed = db.Column(db.Boolean, default=False)

# API Endpoints
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_list = [{"id": b.id, "title": b.title, "author": b.author, "is_borrowed": b.is_borrowed} for b in books]
    return jsonify(book_list)

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added successfully!"}), 201

@app.route('/borrow/<int:book_id>', methods=['PUT'])
def borrow_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found!"}), 404
    if book.is_borrowed:
        return jsonify({"message": "Book is already borrowed!"}), 400
    
    book.is_borrowed = True
    db.session.commit()
    return jsonify({"message": f"You borrowed '{book.title}'."})

@app.route('/return/<int:book_id>', methods=['PUT'])
def return_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found!"}), 404
    if not book.is_borrowed:
        return jsonify({"message": "Book is not currently borrowed!"}), 400
    
    book.is_borrowed = False
    db.session.commit()
    return jsonify({"message": f"You returned '{book.title}'."})
# Add this endpoint to app.py
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found!"}), 404
    return jsonify({"id": book.id, "title": book.title, "author": book.author, "is_borrowed": book.is_borrowed})


@app.route('/books/<int:book_id>', methods=['DELETE'])
def remove_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found!"}), 404
    
    # Safety constraint: Don't delete a book that is currently out!
    if book.is_borrowed:
        return jsonify({"message": "Cannot delete a book that is currently borrowed!"}), 400
    
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": f"'{book.title}' has been permanently removed."})
if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Automatically creates the tables if they don't exist
    app.run(debug=True)
