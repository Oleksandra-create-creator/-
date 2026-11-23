from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EventRegistrationForm

def index(request):
    context = {
        'page_title': 'Головна сторінка',
        'event_name': 'Конференція Python розробників 2024',
        'attendees_count': 150,
        'speakers': ['Олена Петренко', 'Іван Мельник', 'Марія Коваль'],
    }
    return render(request, 'index.html', context)

def register(request):
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, f'Дякуємо, {form.cleaned_data["name"]}! Вашу реєстрацію успішно прийнято.')
            return redirect('index')
    else:
        form = EventRegistrationForm()
    
    return render(request, 'events/register.html', {'form': form})
