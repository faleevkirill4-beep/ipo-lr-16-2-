
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product,Manufacturer,BasketItem,Basket,Category
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,F
from django.contrib import messages


# --------------страницы---------------
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

# --------------Модели---------------
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'shop/category_list.html',{'categories': categories})

# --------------корзина---------------
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




# --------------детали продукта--------------- 
def product_detail(request,pk):
    product = get_object_or_404(Product, pk = pk)

    context = {
        'product': product,
     
    }
    return render(request,'shop/product_detail.html', context)



#---------------добавление в корзину---------------
@login_required
def add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    basket, _ = Basket.objects.get_or_create(user=request.user)
    
    item, created = BasketItem.objects.get_or_create(
        basket=basket,
        product=product,
        defaults={'count': 1}
    )
    
    if not created:
        if item.count < product.count:
            item.count += 1
            item.save()
    
    messages.success(request, f'Товар "{product.name}" добавлен в корзину')
    return redirect('shop:product_list')


#--------------Просмотр корзины----------------
def view_cart(request):
    
    cart = request.session.get('cart', {})
    
    # Рассчитываем итоговую сумму
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    total_items = sum(item['quantity'] for item in cart.values())
    
    context = {
        'cart_items': cart.items(),
        'total_price': total_price,
        'total_items': total_items,
    }
    return render(request, 'shop/cart.html', context)


#-------------удаление товара из корзины-----------------
def remove_from_cart(request, product_id):
   
    cart = request.session.get('cart', {})
    
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        product_name = cart[product_id_str]['name']
        del cart[product_id_str]
        request.session['cart'] = cart
        messages.success(request, f'Товар "{product_name}" удален из корзины')
    
    return redirect('cart')


#--------------Обновление количества товара----------------
def update_cart_quantity(request, product_id):
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        
        if product_id_str in cart:
            if quantity > 0:
                cart[product_id_str]['quantity'] = quantity
                messages.success(request, 'Количество обновлено')
            else:
                del cart[product_id_str]
                messages.success(request, 'Товар удален из корзины')
            
            request.session['cart'] = cart
    
    return redirect('cart')

