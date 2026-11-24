from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

book_tags = db.Table(
    "book_tags",
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, default="")
    books = db.relationship("Book", backref="category", lazy=True, cascade="all, delete")

    def __repr__(self):
        return f"<Category {self.name}>"


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    slug = db.Column(db.String(40), unique=True, nullable=False)
    color = db.Column(db.String(7), default="#000000")

    def __repr__(self):
        return f"<Tag {self.name}>"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, default=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    tags = db.relationship("Tag", secondary=book_tags, backref="books", lazy="subquery")
    loans = db.relationship("Loan", backref="book", lazy=True)
    __table_args__ = (db.UniqueConstraint("title", "category_id", name="uniq_title_category"),)

    def __repr__(self):
        return f"<Book {self.title} ({self.year})>"


class Reader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    registered_at = db.Column(db.Date, default=date.today)
    profile = db.relationship("ReaderProfile", backref="reader", uselist=False, cascade="all, delete")
    loans = db.relationship("Loan", backref="reader", lazy=True, cascade="all, delete")

    def __repr__(self):
        return f"<Reader {self.name}>"


class ReaderProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(60), nullable=False)
    reader_id = db.Column(db.Integer, db.ForeignKey("reader.id"), unique=True, nullable=False)

    def __repr__(self):
        return f"<Profile {self.city}>"


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    reader_id = db.Column(db.Integer, db.ForeignKey("reader.id"), nullable=False)
    loan_date = db.Column(db.Date, default=date.today)
    due_date = db.Column(db.Date, nullable=False)
    returned = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Loan {self.book_id}->{self.reader_id}>"
