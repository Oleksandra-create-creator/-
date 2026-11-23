import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from datetime import date, timedelta
from django.db.models import Q, Count, Avg, Max
from catalog.models import Category, Tag, Book, Reader, ReaderProfile, Loan


def run():
    Loan.objects.all().delete()
    Book.objects.all().delete()
    Category.objects.all().delete()
    Tag.objects.all().delete()
    Reader.objects.all().delete()

    fantasy = Category.objects.create(name="Фантастика", slug="fantasy", description="Фантастичні твори")
    classic = Category.objects.create(name="Класика", slug="classic", description="Класична література")
    tag = Tag.objects.create(name="Епіка", slug="epic")

    dune = Book.objects.create(title="Дюна", year=1965, category=fantasy)
    dune.tags.add(tag)
    Book.objects.create(title="Кобзар", year=1840, category=classic)
    Book.objects.create(title="Нейромант", year=1984, category=fantasy, available=False)

    reader = Reader.objects.create(name="Олена", email="olena@example.com")
    ReaderProfile.objects.create(reader=reader, phone="+380501112233", city="Київ")
    Loan.objects.create(book=dune, reader=reader, due_date=date.today() + timedelta(days=14))

    print("CREATE:", dune)
    print("READ:", Book.objects.get(pk=dune.pk))
    dune.year = 1966
    dune.save()
    print("UPDATE:", dune.year)

    print("FILTER:", list(Book.objects.filter(year__gte=1960).values_list("title", flat=True)))
    print("EXCLUDE:", list(Book.objects.exclude(available=True).values_list("title", flat=True)))
    print("Q OR:", list(Book.objects.filter(Q(year__lt=1900) | Q(category__name="Фантастика")).values_list("title", flat=True)))

    print("AGGREGATE:", Book.objects.aggregate(avg_year=Avg("year"), max_year=Max("year")))
    for c in Category.objects.annotate(books_count=Count("books")):
        print("ANNOTATE:", c.name, c.books_count)

    print("REVERSE FK:", list(fantasy.books.values_list("title", flat=True)))
    print("REVERSE M2M:", list(tag.books.values_list("title", flat=True)))
    print("ONETOONE:", reader.profile.city)

    for book in Book.objects.select_related("category").prefetch_related("tags"):
        print("OPTIMIZED:", book.title, book.category.name, [t.name for t in book.tags.all()])

    temporary = Book.objects.create(title="Тимчасова", year=2000, category=classic)
    temporary.delete()
    print("DELETE OK, залишилось:", Book.objects.count())


if __name__ == "__main__":
    run()
