# fill_db.py
import os
import django
from decimal import Decimal

# Настройка Django окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_shop.settings')
django.setup()

from django.contrib.auth.models import User
from shop.models import Category, Manufacturer, Product, Basket, BasketItem

def fill_database():
    print("Начинаем заполнение базы данных...")
    
    # ========== 1. СОЗДАЕМ КАТЕГОРИИ (10 штук) ==========
    categories_data = [
        {"name": "Стратегические игры", "description": "Игры, требующие стратегического мышления и планирования"},
        {"name": "Экономические игры", "description": "Игры про бизнес, торговлю и управление ресурсами"},
        {"name": "Карточные игры", "description": "Игры с использованием специальных колод карт"},
        {"name": "Кооперативные игры", "description": "Игры, где игроки объединяются против игры"},
        {"name": "Детективные игры", "description": "Игры про расследования и загадки"},
        {"name": "Приключенческие игры", "description": "Игры с сюжетом и приключениями"},
        {"name": "Фэнтези игры", "description": "Игры в мире магии и фэнтези"},
        {"name": "Научно-фантастические игры", "description": "Игры про космос и будущее"},
        {"name": "Семейные игры", "description": "Игры для всей семьи, простые и веселые"},
        {"name": "Вечериночные игры", "description": "Игры для больших компаний и вечеринок"},
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data["name"],
            defaults={"description": cat_data["description"]}
        )
        categories.append(category)
        print(f"✅ Создана категория: {category.name}")
    
    # ========== 2. СОЗДАЕМ ПРОИЗВОДИТЕЛЕЙ (5 штук) ==========
    manufacturers_data = [
        {"name": "Hasbro", "country": "США", "description": "Крупнейший производитель настольных игр"},
        {"name": "Hobby World", "country": "Россия", "description": "Российский издатель настольных игр"},
        {"name": "Cosmodrome Games", "country": "Россия", "description": "Издатель настольных игр из Москвы"},
        {"name": "Zvezda", "country": "Россия", "description": "Известный производитель игр и моделей"},
        {"name": "Ravensburger", "country": "Германия", "description": "Немецкий производитель качественных игр"},
    ]
    
    manufacturers = []
    for man_data in manufacturers_data:
        manufacturer, created = Manufacturer.objects.get_or_create(
            name=man_data["name"],
            defaults={
                "country": man_data["country"],
                "description": man_data["description"]
            }
        )
        manufacturers.append(manufacturer)
        print(f"✅ Создан производитель: {manufacturer.name}")
    
    # ========== 3. СОЗДАЕМ ТОВАРЫ (34 штуки) ==========
    products_data = [
        # Стратегические игры
        {"name": "Колонизаторы", "description": "Классическая стратегическая игра о колонизации острова", "price": 2990, "count": 15, "category": "Стратегические игры", "manufacturer": "Cosmodrome Games"},
        {"name": "Манчкин", "description": "Юмористическая карточная игра о подземельях", "price": 1990, "count": 25, "category": "Карточные игры", "manufacturer": "Hobby World"},
        {"name": "Ticket to Ride", "description": "Стратегия о строительстве железных дорог", "price": 3990, "count": 10, "category": "Стратегические игры", "manufacturer": "Ravensburger"},
        
        # Экономические игры
        {"name": "Монополия", "description": "Классическая экономическая игра о недвижимости", "price": 2500, "count": 30, "category": "Экономические игры", "manufacturer": "Hasbro"},
        {"name": "Каркассон", "description": "Средневековая стратегия о строительстве замков", "price": 2790, "count": 18, "category": "Стратегические игры", "manufacturer": "Cosmodrome Games"},
        
        # Карточные игры
        {"name": "UNO", "description": "Популярная карточная игра для всей семьи", "price": 890, "count": 45, "category": "Карточные игры", "manufacturer": "Hasbro"},
        {"name": "Имаджинариум", "description": "Игра на ассоциации и воображение", "price": 2200, "count": 12, "category": "Вечериночные игры", "manufacturer": "Cosmodrome Games"},
        
        # Кооперативные игры
        {"name": "Запретный остров", "description": "Кооперативная игра о спасении сокровищ", "price": 1890, "count": 8, "category": "Кооперативные игры", "manufacturer": "Hobby World"},
        {"name": "Пандемия", "description": "Кооперативная игра о борьбе с болезнями", "price": 3290, "count": 7, "category": "Кооперативные игры", "manufacturer": "Hobby World"},
        
        # Детективные игры
        {"name": "Cluedo", "description": "Детективная игра о расследовании убийства", "price": 2690, "count": 9, "category": "Детективные игры", "manufacturer": "Hasbro"},
        
        # Приключенческие игры
        {"name": "Дженга", "description": "Игра на ловкость и баланс", "price": 1200, "count": 35, "category": "Семейные игры", "manufacturer": "Hasbro"},
        {"name": "Activity", "description": "Командная игра на объяснение слов", "price": 2450, "count": 14, "category": "Вечериночные игры", "manufacturer": "Ravensburger"},
        
        # Фэнтези игры
        {"name": "Ведьмак", "description": "Настольная игра по мотивам Ведьмака", "price": 4500, "count": 5, "category": "Фэнтези игры", "manufacturer": "Hobby World"},
        {"name": "Берсерк", "description": "Карточная дуэльная игра в славянском фэнтези", "price": 1590, "count": 20, "category": "Фэнтези игры", "manufacturer": "Hobby World"},
        
        # Научно-фантастические игры
        {"name": "Cosmic Encounter", "description": "Космическая стратегия с уникальными расами", "price": 4990, "count": 6, "category": "Научно-фантастические игры", "manufacturer": "Cosmodrome Games"},
        
        # Семейные игры
        {"name": "Alias", "description": "Игра на объяснение слов", "price": 1890, "count": 22, "category": "Семейные игры", "manufacturer": "Ravensburger"},
        {"name": "Доббль", "description": "Быстрая игра на поиск совпадений", "price": 990, "count": 40, "category": "Семейные игры", "manufacturer": "Ravensburger"},
        
        # Еще игры для заполнения до 34
        {"name": "Шакал", "description": "Стратегия о поиске сокровищ на острове", "price": 3490, "count": 11, "category": "Стратегические игры", "manufacturer": "Zvezda"},
        {"name": "Свинтус", "description": "Веселая карточная игра", "price": 790, "count": 28, "category": "Карточные игры", "manufacturer": "Hobby World"},
        {"name": "Мафия", "description": "Психологическая командная игра", "price": 990, "count": 33, "category": "Вечериночные игры", "manufacturer": "Cosmodrome Games"},
        {"name": "Кодовые имена", "description": "Игра на ассоциации и логику", "price": 1790, "count": 16, "category": "Кооперативные игры", "manufacturer": "Hobby World"},
        {"name": "Эволюция", "description": "Стратегия о развитии видов", "price": 2590, "count": 13, "category": "Стратегические игры", "manufacturer": "Hobby World"},
        {"name": "Скрэббл", "description": "Словесная игра на составление слов", "price": 2100, "count": 17, "category": "Семейные игры", "manufacturer": "Hasbro"},
        {"name": "Риск", "description": "Стратегия о завоевании мира", "price": 3990, "count": 8, "category": "Стратегические игры", "manufacturer": "Hasbro"},
        {"name": "Тик-Так-Бум", "description": "Динамичная игра со словами", "price": 1490, "count": 24, "category": "Вечериночные игры", "manufacturer": "Ravensburger"},
        {"name": "Зельеварение", "description": "Игра о создании магических зелий", "price": 2190, "count": 19, "category": "Фэнтези игры", "manufacturer": "Hobby World"},
        {"name": "7 Wonders", "description": "Стратегия о развитии цивилизаций", "price": 4290, "count": 9, "category": "Стратегические игры", "manufacturer": "Cosmodrome Games"},
        {"name": "Каркассон: Королевский подарок", "description": "Расширение для Каркассона", "price": 1490, "count": 12, "category": "Стратегические игры", "manufacturer": "Cosmodrome Games"},
        {"name": "Бэнг!", "description": "Карточная игра в стиле вестерн", "price": 1690, "count": 21, "category": "Карточные игры", "manufacturer": "Hobby World"},
        {"name": "Фото-Фокус", "description": "Игра на скорость и внимание", "price": 890, "count": 26, "category": "Семейные игры", "manufacturer": "Zvezda"},
        {"name": "Цитадели", "description": "Стратегия о строительстве города", "price": 1990, "count": 15, "category": "Экономические игры", "manufacturer": "Hobby World"},
        {"name": "Диксит", "description": "Игра на ассоциации с красивыми картами", "price": 2490, "count": 14, "category": "Кооперативные игры", "manufacturer": "Hobby World"},
        {"name": "Путь принцессы", "description": "Семейная игра с романтическим сюжетом", "price": 1890, "count": 18, "category": "Семейные игры", "manufacturer": "Ravensburger"},
        {"name": "Зомбицид", "description": "Кооперативная игра про зомби", "price": 3490, "count": 7, "category": "Кооперативные игры", "manufacturer": "Zvezda"},
        {"name": "Тайны Гоголя", "description": "Детективная игра по мотивам Гоголя", "price": 2790, "count": 6, "category": "Детективные игры", "manufacturer": "Hobby World"},
    ]
    
    products = []
    for prod_data in products_data:
        category = Category.objects.get(name=prod_data["category"])
        manufacturer = Manufacturer.objects.get(name=prod_data["manufacturer"])
        
        product, created = Product.objects.get_or_create(
            name=prod_data["name"],
            defaults={
                "description": prod_data["description"],
                "price": Decimal(prod_data["price"]),
                "count": prod_data["count"],
                "category": category,
                "manufacturer": manufacturer
            }
        )
        products.append(product)
        if created:
            print(f"✅ Создан товар: {product.name}")
        else:
            print(f"⚠️ Товар уже существует: {product.name}")
    
    # ========== 4. СОЗДАЕМ ПОЛЬЗОВАТЕЛЕЙ (5 штук) ==========
    users_data = [
        {"username": "alex_gamer", "email": "alex@example.com", "password": "alex123456", "first_name": "Алексей", "last_name": "Игроков"},
        {"username": "marina_player", "email": "marina@example.com", "password": "marina123456", "first_name": "Марина", "last_name": "Настольная"},
        {"username": "dmitry_board", "email": "dmitry@example.com", "password": "dmitry123456", "first_name": "Дмитрий", "last_name": "Стратегов"},
        {"username": "elena_games", "email": "elena@example.com", "password": "elena123456", "first_name": "Елена", "last_name": "Игровая"},
        {"username": "pavel_dice", "email": "pavel@example.com", "password": "pavel123456", "first_name": "Павел", "last_name": "Кубиков"},
    ]
    
    users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data["username"],
            defaults={
                "email": user_data["email"],
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"]
            }
        )
        if created:
            user.set_password(user_data["password"])
            user.save()
            users.append(user)
            print(f"✅ Создан пользователь: {user.username} (пароль: {user_data['password']})")
        else:
            users.append(user)
            print(f"⚠️ Пользователь уже существует: {user.username}")
    
    # ========== 5. ДОБАВЛЯЕМ НЕСКОЛЬКО ТОВАРОВ В КОРЗИНЫ ==========
    print("\nДобавляем товары в корзины пользователей...")
    
    for i, user in enumerate(users[:3]):  # Для первых 3 пользователей
        basket, created = Basket.objects.get_or_create(user=user)
        
        # Добавляем 2-3 случайных товара в корзину
        for j in range(3):
            product = products[j * 3 + i * 2 % len(products)]
            count = (i + j) % 3 + 1
            
            item, created = BasketItem.objects.get_or_create(
                basket=basket,
                product=product,
                defaults={"count": count}
            )
            
            if not created:
                item.count = count
                item.save()
            
            print(f"  - {user.username}: {product.name} x{count}")
    
    # ========== ВЫВОД ИТОГОВ ==========
    print("\n" + "="*50)
    print("БАЗА ДАННЫХ УСПЕШНО ЗАПОЛНЕНА!")
    print("="*50)
    print(f"📊 Категории: {Category.objects.count()}/10")
    print(f"🏭 Производители: {Manufacturer.objects.count()}/5")
    print(f"🎲 Товары: {Product.objects.count()}/34")
    print(f"👤 Пользователи: {User.objects.count()} (из них активных: {User.objects.filter(is_active=True).count()})")
    print(f"🛒 Корзины: {Basket.objects.count()}")
    print(f"📦 Товаров в корзинах: {BasketItem.objects.count()}")
    print("="*50)
    
    print("\n📝 Данные для входа в админку:")
    print("   URL: http://127.0.0.1:8000/admin/")
    print("   Логин: admin (если создавали) или любой из пользователей")
    print("\n👤 Тестовые пользователи (логин/пароль):")
    for user in users:
        print(f"   - {user.username} / {user.username.replace('_', '')}123456")

if __name__ == "__main__":
    fill_database()