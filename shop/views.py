
from django.shortcuts import render

def index(request):
    "Главная страница с ссылками"
    return render(request, 'shop/index.html')

def about(request):
    context = {
        'student_name': 'Фалеев Кирилл',
        'group': '88ТП',
        'year': 2026

    }
    return render(request, 'shop/about.html', context)

def shop_info(request):
    "Страница о магазине"
    return render(request, 'shop/shop_info.html')
'''
from django.http import HttpResponse

def index(request):
    html = "<h1>Главная страница</h1><nav><a href='/about/'>Об авторе</a> | <a href='/shop-info/'>О магазине</a></nav>"
    return HttpResponse(html)

def about(request):
    html = "<h1>Об авторе</h1><p>Студент: [Ваше имя]</p><nav><a href='/'>На главную</a></nav>"
    return HttpResponse(html)

def shop_info(request):
    html = "<h1>О магазине</h1><p>Магазин настольных игр</p><nav><a href='/'>На главную</a></nav>"
    return HttpResponse(html)
'''