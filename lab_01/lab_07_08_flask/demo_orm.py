from datetime import date, timedelta
from sqlalchemy import func, or_
from sqlalchemy.orm import joinedload
from app import create_app
from models import db, Category, Tag, Book, Reader, ReaderProfile, Loan


def run():
    app = create_app({"SQLALCHEMY_DATABASE_URI": "sqlite:///demo.db"})
    with app.app_context():
        db.drop_all()
        db.create_all()

        fantasy = Category(name="Фантастика", slug="fantasy", description="Твори")
        classic = Category(name="Класика", slug="classic", description="Класика")
        tag = Tag(name="Епіка", slug="epic")
        db.session.add_all([fantasy, classic, tag])
        db.session.commit()

        dune = Book(title="Дюна", year=1965, category=fantasy, tags=[tag])
        db.session.add(dune)
        db.session.add(Book(title="Кобзар", year=1840, category=classic))
        reader = Reader(name="Олена", email="olena@example.com")
        db.session.add(reader)
        db.session.commit()

        db.session.add(ReaderProfile(phone="+380501112233", city="Київ", reader_id=reader.id))
        db.session.add(Loan(book_id=dune.id, reader_id=reader.id, due_date=date.today() + timedelta(days=14)))
        db.session.commit()

        print("CREATE:", dune)
        print("READ:", db.session.get(Book, dune.id))
        dune.year = 1966
        db.session.commit()
        print("UPDATE:", dune.year)

        print("FILTER:", [b.title for b in Book.query.filter(Book.year >= 1960).all()])
        print("EXCLUDE:", [b.title for b in Book.query.filter(Book.available.is_(False)).all()])
        print("OR:", [b.title for b in Book.query.filter(or_(Book.year < 1900, Book.title == "Дюна")).all()])
        print("AGGREGATE:", db.session.query(func.count(Book.id), func.avg(Book.year)).one())
        print("ANNOTATE:", db.session.query(Category.name, func.count(Book.id)).join(Book).group_by(Category.name).all())
        print("REVERSE FK:", [b.title for b in fantasy.books])
        print("REVERSE M2M:", [b.title for b in tag.books])
        print("ONETOONE:", reader.profile.city)
        print("EAGER:", [b.category.name for b in Book.query.options(joinedload(Book.category)).all()])

        try:
            db.session.add(Book(title="Перша", year=2001, category_id=classic.id))
            db.session.add(Book(title="Друга", year=2002, category_id=None))
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            print("ROLLBACK:", type(error).__name__)

        print("Після rollback книг:", Book.query.count())

        db.session.delete(dune)
        db.session.commit()
        print("DELETE OK, книг:", Book.query.count())


if __name__ == "__main__":
    run()
