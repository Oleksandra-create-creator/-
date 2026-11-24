from flask import Flask, jsonify, request, abort
from flask_migrate import Migrate
from models import db, Book, Category
from services import generate_code, notify_external


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite:///library.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY="dev-only-key",
    )
    if config:
        app.config.update(config)

    db.init_app(app)
    Migrate(app, db)

    @app.get("/books")
    def book_list():
        books = Book.query.all()
        return jsonify([{"id": b.id, "title": b.title, "year": b.year} for b in books])

    @app.get("/books/<int:book_id>")
    def book_detail(book_id):
        book = db.session.get(Book, book_id)
        if book is None:
            abort(404)
        return jsonify(id=book.id, title=book.title, category=book.category.name)

    @app.post("/books")
    def book_create():
        data = request.get_json(silent=True) or {}
        if not data.get("title") or not data.get("category_id"):
            abort(400)
        book = Book(title=data["title"], year=int(data.get("year", 2000)), category_id=data["category_id"])
        db.session.add(book)
        db.session.commit()
        return jsonify(id=book.id, code=generate_code()), 201

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
