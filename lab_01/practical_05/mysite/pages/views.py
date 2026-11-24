from django.http import HttpResponse

def index(request):
    html = "<h1>Головна сторінка</h1><p>Ласкаво просимо до мого Django проєкту.</p><ul><li>Пункт 1</li><li>Пункт 2</li><li>Пункт 3</li></ul>"
    return HttpResponse(html)

def about(request):
    html = "<h1>Про проєкт</h1><p>Курс: Веб-розробка на Python</p><p>Практична робота №5</p><p>Студент: [Твоє Ім'я]</p>"
    return HttpResponse(html)

def contact(request):
    name = request.GET.get('name')
    if name:
        return HttpResponse(f"<h1>Привіт, {name}!</h1>")
    return HttpResponse("<h1>Контактна сторінка</h1><p>Будь ласка, додайте ?name=ВашеІм'я до URL.</p>")
