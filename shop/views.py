
from django.shortcuts import render, get_object_or_404
from .models import Product,Manufacturer,Element_bascet,Bascet,Category
from django.contrib.auth.decorators import login_required

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

#модели 
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'shop/category_list.html',{'categories': categories})


# корзина
@login_required
def bascet(request):
    try:
        bascets = Bascet.objects.get(user=request.user)
        elements = bascets.elements.all()
        
        # Вычисляем общую стоимость
        total_coast = 0
        for element in elements:
            total_coast += element.Price_element()
            
    except Bascet.DoesNotExist:
        bascets = None
        elements = []
        total_coast = 0
    
    return render(request, 'shop/bascet.html', {
        'bascet': bascets,
        'elements': elements,
        'total_coast': total_coast
    })