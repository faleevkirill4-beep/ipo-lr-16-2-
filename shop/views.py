
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product,Manufacturer,BasketItem,Basket,Category
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,F,Q
from django.contrib import messages
from .utils import create_excel_receipt
from django.core.mail import EmailMessage
from my_shop import settings
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

#фильтрация  
    category_id = request.GET.get('category')
    search_query = request.GET.get('search','').strip()

#поиск по категории 
    if category_id:
        products = products.filter(category_id = category_id)
#Поиск по названию и описанию продукта
    if search_query:
        products = products.filter(
            Q(name__icontains = search_query)|
            Q(description__icontains = search_query)
        )
    
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
    return redirect('product_list')



#-------------удаление товара из корзины-----------------
@login_required
def remove_from_basket(request, item_id):
    item = get_object_or_404(BasketItem, id=item_id, basket__user=request.user)
    product_name = item.product.name
    item.delete()
    messages.success(request, f'Товар "{product_name}" удален из корзины')
    return redirect('basket')
#---------------Обновление количества товара в корзине---------------
@login_required
def update_basket_quantity(request, item_id):
    
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (TypeError, ValueError):
            messages.error(request, 'Укажите корректное количество')
            return redirect('basket')
        
        item = get_object_or_404(BasketItem, id=item_id, basket__user=request.user)
        
        if quantity <= 0:
            item.delete()
            messages.success(request, f'Товар "{item.product.name}" удален')
        elif quantity > item.product.count:
            messages.error(request, f'Доступно только {item.product.count} шт.')
        else:
            item.count = quantity
            item.save()
            messages.success(request, f'Количество обновлено')
        
        return redirect('basket')
    
    return redirect('basket')



#-----------оформление заказа------------
@login_required
def checkout(request):
    """Оформление заказа"""
    
    if request.method == 'POST':
        # Получаем корзину
        basket = Basket.objects.filter(user_id=request.user.id).first()
        
        if basket:
            items = BasketItem.objects.filter(basket_id=basket.id)
            
            # Считаем сумму
            total = sum(item.product.price * item.count for item in items)
            
            # Текст письма
            message = f"Спасибо за покупку, {request.user.username}!\n"
            message += f"Телефон: {request.POST.get('phone')}\n"
            message += f"Адрес: {request.POST.get('address')}\n"
            message += "Ваши товары:\n"
            
            for item in items:
                message += f"- {item.product.name} x {item.count} = {item.product.price * item.count} руб.\n"
            
            message += f"\nИтого: {total} руб.\nСпасибо!"
            
            # Отправляем
            email = EmailMessage(
                subject=f"Заказ от {request.user.username}",
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[request.POST.get('email')]
            )
            excel_file = create_excel_receipt(user=request.user,items=items,total_price = total)
            # excel_file - это BytesIO объект
            email.attach('чек.xlsx', excel_file.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            email.send()
            
            # Очищаем корзину
            items.delete()
            basket.delete()
            
            messages.success(request, 'Заказ оформлен!')
        
        return redirect('product_list')
    
    return render(request, 'shop/checkout.html')
            
