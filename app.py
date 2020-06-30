from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'books.sqlite')

db = SQLAlchemy(app)

ma = Marshmallow(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(400))

    def __init__(self, name, description):
        self.name = name
        self.description = description


class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')


book_schema = BookSchema()
books_schema = BookSchema(many=True)


@app.route('/book', methods=['POST'])
def add_book():
    request_data = request.json
    name = request_data["name"]
    description = request_data["description"]

    new_book = Book(name, description)

    db.session.add(new_book)
    db.session.commit()

    return "added"


@app.route('/book', methods=["GET"])
def get_books():
    all_books = Book.query.all()
    result = books_schema.dump(all_books)

    return jsonify(result)


@app.route('/book/<id>', methods=["GET"])
def get_book_by_id(id):
    book = Book.query.get(id)
    result = book_schema.dump(book)

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, port=3020)