
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product,Manufacturer,BasketItem,Basket,Category
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,F,Q
from django.contrib import messages
from .utils import create_excel_receipt
from django.core.mail import EmailMessage
from my_shop import settings
from .serializers import  ProductSerializer,CategorySerializer,ManufacturerSerializer,BasketSerializer,BasketItemSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import uuid

# --------------страницы---------------
def index(request):
    "Главная страница с ссылками"
    popular_products = Product.objects.all().order_by('-id')[:6]

    categories = Category.objects.all()

    context = {
        'popular_products':popular_products,
        'categories':categories,
    }

    return render(request, 'shop/index.html',context)

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
    """Страница каталога товаров с фильтрацией и пагинацией"""
    
    # Начинаем со всех товаров
    products = Product.objects.all()
    
    # Фильтр по категории
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Фильтр по производителю
    manufacturer_id = request.GET.get('manufacturer')
    if manufacturer_id:
        products = products.filter(manufacturer_id=manufacturer_id)
    
    # Поиск по названию
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    
    # Пагинация (9 товаров на странице)
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Получаем все категории и производителей для фильтров
    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()
    
    context = {
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'categories': categories,
        'manufacturers': manufacturers,
    }
    return render(request, 'shop/product_list.html', context)

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
def product_detail(request, pk):
    """Детальная страница товара"""
    product = get_object_or_404(Product, pk=pk)
    
    # Похожие товары (из той же категории, исключая текущий)
    similar_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'similar_products': similar_products,
    }
    return render(request, 'shop/product_detail.html', context)


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


@login_required
def checkout(request):
    """Оформление заказа"""
    
    # GET запрос - показываем форму
    if request.method == 'GET':
        # Получаем корзину для отображения в форме
        basket = Basket.objects.filter(user=request.user).first()
        
        if not basket:
            messages.warning(request, 'Ваша корзина пуста')
            return redirect('basket')
        
        items = BasketItem.objects.filter(basket=basket)
        
        if not items:
            messages.warning(request, 'Ваша корзина пуста')
            return redirect('basket')
        
        # Считаем сумму
        total = sum(item.product.price * item.count for item in items)
        
        context = {
            'items': items,
            'total': total,
        }
        return render(request, 'shop/checkout.html', context)
    
    # POST запрос - оформляем заказ
    if request.method == 'POST':
        # Получаем данные из формы
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        email = request.POST.get('email', '').strip()
        comment = request.POST.get('comment', '').strip()
        
        # Проверяем заполнение обязательных полей
        if not phone:
            messages.error(request, 'Пожалуйста, укажите номер телефона')
            return redirect('checkout')
        
        if not address:
            messages.error(request, 'Пожалуйста, укажите адрес доставки')
            return redirect('checkout')
        
        if not email:
            messages.error(request, 'Пожалуйста, укажите email для получения чека')
            return redirect('checkout')
        
        # Проверка формата email
        if '@' not in email or '.' not in email:
            messages.error(request, 'Пожалуйста, укажите корректный email адрес')
            return redirect('checkout')
        
        # Получаем корзину
        basket = Basket.objects.filter(user=request.user).first()
        
        if not basket:
            messages.warning(request, 'Корзина пуста')
            return redirect('basket')
        
        items = BasketItem.objects.filter(basket=basket)
        
        if not items:
            messages.warning(request, 'Корзина пуста')
            return redirect('basket')
        
        # Проверка наличия товаров на складе
        for item in items:
            if item.count > item.product.count:
                messages.error(request, f'Товара "{item.product.name}" недостаточно на складе. Доступно: {item.product.count} шт.')
                return redirect('basket')
        
        # Считаем сумму
        total = sum(item.product.price * item.count for item in items)
        
        # Генерируем номер заказа
        order_id = str(uuid.uuid4())[:8].upper()
        
        # Формируем текст письма
        message = f"""
Здравствуйте, {request.user.username}!

Ваш заказ #{order_id} успешно оформлен!

📋 ДЕТАЛИ ЗАКАЗА:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📞 Телефон: {phone}
📍 Адрес доставки: {address}
📧 Email: {email}
💬 Комментарий: {comment if comment else 'Нет'}

🛒 СОСТАВ ЗАКАЗА:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        for item in items:
            item_total = item.product.price * item.count
            message += f"• {item.product.name} x {item.count} шт. = {item_total:,.2f} руб.\n"
        
        message += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 ИТОГО К ОПЛАТЕ: {total:,.2f} руб.

📅 Дата заказа: {datetime.now().strftime("%d.%m.%Y %H:%M")}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Чек в формате Excel прикреплен к этому письму.

Спасибо за покупку!
С уважением, команда магазина "Настольные игры".
"""
        
        # Отправляем email
        try:
            # Создаем письмо
            email_message = EmailMessage(
                subject=f"✅ Подтверждение заказа #{order_id}",
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
                reply_to=[settings.DEFAULT_FROM_EMAIL],
            )
            
            # Делаем письмо в кодировке UTF-8
            email_message.encoding = 'utf-8'
            
            # Создаем и прикрепляем Excel чек
            excel_file = create_excel_receipt(
                user=request.user,
                items=items,
                total_price=total,
                phone=phone,
                address=address,
                order_id=order_id
            )
            
            email_message.attach(
                f'чек_заказ_{order_id}.xlsx', 
                excel_file.getvalue(), 
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
            # Отправляем
            email_message.send()
            
            messages.success(request, f'✅ Заказ #{order_id} успешно оформлен! Чек отправлен на {email}')
            
        except Exception as e:
            messages.error(request, f'❌ Ошибка при оформлении заказа: {str(e)}')
            return redirect('basket')
        
        # Уменьшаем количество товара на складе
        for item in items:
            product = item.product
            product.count -= item.count
            product.save()
        
        # Очищаем корзину
        items.delete()
        basket.delete()
        
        return redirect('product_list')
    
    return redirect('basket')
#регистрация 
def register(request):
    """Регистрация нового пользователя"""
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


#-------------API-------------------


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]  # Только авторизованные

class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = [IsAuthenticated]  

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]  

class BasketViewSet(viewsets.ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = [IsAuthenticated]  
class BasketItemViewSet(viewsets.ModelViewSet):
    queryset = BasketItem.objects.all()
    serializer_class = BasketItemSerializer
    permission_classes = [IsAuthenticated]  


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_add_to_basket(request):
    """API для добавления товара в корзину"""
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)
    
    if not product_id:
        return Response({'error': 'product_id обязателен'}, status=status.HTTP_400_BAD_REQUEST)
    
    product = get_object_or_404(Product, id=product_id)
    basket, _ = Basket.objects.get_or_create(user=request.user)
    
    cart_item, created = BasketItem.objects.get_or_create(
        basket=basket,
        product=product,
        defaults={'count': quantity}
    )
    
    if not created:
        if cart_item.count + quantity <= 99:
            cart_item.count += quantity
            cart_item.save()
        else:
            return Response({'error': 'Нельзя добавить больше 99 товаров'}, status=status.HTTP_400_BAD_REQUEST)
    
    # ВАРИАНТЫ РАБОТАЮЩЕГО КОДА:
    
    # Вариант 1: Стандартный
    result = basket.items.aggregate(total=Sum('count'))
    total_items = result['total'] if result['total'] is not None else 0
    
    # Вариант 2: Более короткий
    # total_items = basket.items.aggregate(total=Sum('count')).get('total') or 0
    
    # Вариант 3: Без агрегации (циклом)
    # total_items = 0
    # for item in basket.items.all():
    #     total_items += item.count
    
    return Response({
        'message': f'Товар "{product.name}" добавлен в корзину',
        'total_items': total_items
    })