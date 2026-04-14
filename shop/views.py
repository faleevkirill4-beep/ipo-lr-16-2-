
from django.shortcuts import render, get_object_or_404
from .models import Product,Manufacturer,BasketItem,Basket,Category
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,F
#страницы

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
def basket(request):
    try:
        baskets = Basket.objects.prefetch_related('items__product').get(user=request.user)
        
        elements = baskets.items.all()
    #подсчет общей стоймости 

        total_cost = elements.aggregate(
            total=Sum(F('count') * F('product__price'))
        )['total'] or 0



            
    except Basket.DoesNotExist:
        baskets = None
        elements = []
        total_cost = 0
    
    return render(request, 'shop/basket.html', {
        'basket': baskets,
        'elements': elements,
        'total_cost': total_cost,
    })

def product_detail(request,pk):
    product = get_object_or_404(Product, id = pk)

    context = {
        'product': product,
     
    }
    return render(request,'shop/product_detail.html', context)
