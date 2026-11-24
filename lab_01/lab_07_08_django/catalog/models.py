from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=7, default="#000000")

    class Meta:
        ordering = ["name"]
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=150)
    year = models.IntegerField()
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="books")
    tags = models.ManyToManyField(Tag, blank=True, related_name="books")

    class Meta:
        ordering = ["-year", "title"]
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        constraints = [models.UniqueConstraint(fields=["title", "category"], name="uniq_title_category")]

    def __str__(self):
        return f"{self.title} ({self.year})"


class Reader(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    registered_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Читач"
        verbose_name_plural = "Читачі"

    def __str__(self):
        return self.name


class ReaderProfile(models.Model):
    reader = models.OneToOneField(Reader, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=60)
    address = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["reader__name"]
        verbose_name = "Профіль читача"
        verbose_name_plural = "Профілі читачів"

    def __str__(self):
        return f"{self.reader.name} — {self.city}"


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="loans")
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name="loans")
    loan_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned = models.BooleanField(default=False)

    class Meta:
        ordering = ["-loan_date"]
        verbose_name = "Видача"
        verbose_name_plural = "Видачі"

    def __str__(self):
        return f"{self.book.title} → {self.reader.name}"
