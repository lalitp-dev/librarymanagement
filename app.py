import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app) 

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:lalit1@localhost/library_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize Groq Client securely on the backend
client = Groq(api_key=os.environ.get("GROQ_API_KEY")) if os.environ.get("GROQ_API_KEY") else None

# --- Database Model ---
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    is_borrowed = db.Column(db.Boolean, default=False)

# --- API Endpoints ---
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
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found!"}), 404
    return jsonify({"id": book.id, "title": book.title, "author": book.author, "is_borrowed": book.is_borrowed})
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

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found!"}), 404
    if book.is_borrowed:
        return jsonify({"message": "Cannot delete a borrowed book!"}), 400
        
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book permanently removed."})

@app.route('/summary/<int:book_id>', methods=['GET'])
def get_book_summary(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found!"}), 404
        
    if not client:
        return jsonify({"message": "Groq AI configuration missing on server."}), 503
        
    try:
        prompt = f"Provide a concise, engaging summary of the book '{book.title}' by {book.author}. Keep it to two paragraphs and use markdown formatting."
        
        # Call Groq's Llama 3 API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant", 
        )
        
        return jsonify({"summary": chat_completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"message": f"AI Engine Error: {str(e)}"}), 503

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
