from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Category
from .services import generate_code, notify_external


def book_list(request):
    books = Book.objects.select_related("category").prefetch_related("tags")
    return render(request, "catalog/book_list.html", {"books": books})


def book_detail(request, pk):
    book = get_object_or_404(Book.objects.select_related("category"), pk=pk)
    return render(request, "catalog/book_detail.html", {"book": book})


def book_create(request):
    if request.method == "POST":
        category = get_object_or_404(Category, pk=request.POST["category"])
        book = Book.objects.create(
            title=request.POST["title"],
            year=int(request.POST["year"]),
            category=category,
        )
        messages.success(request, f"Книгу створено. Код: {generate_code()}")
        notify_external(book.title)
        return redirect("book_list")
    return render(request, "catalog/book_form.html", {"categories": Category.objects.all()})
