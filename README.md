# ipo-lr-16-2-
# Интернет-магазин электроники

## Описание проекта
Веб-приложение на Django, представляющее собой интернет-магазин электроники. 
Проект создан в рамках лабораторной работы по изучению основ Django.

## Страницы магазина
1. **Главная страница** (`/`) - навигация по разделам сайта
2. **О магазине** (`/shop-info/`) - информация о тематике магазина и ассортименте
3. **Об авторе** (`/about/`) - информация о разработчике

## Технологии
- Python 3.x
- Django 4.x
- SQLite (база данных по умолчанию)

## Установка и запуск
1. Клонировать репозиторий
2. Создать виртуальное окружение: `python -m venv venv`
3. Активировать виртуальное окружение
4. Установить зависимости: `pip install -r requirements.txt`
5. Применить миграции: `python manage.py migrate`
6. Запустить сервер: `python manage.py runserver`
7. Открыть в браузере: http://127.0.0.1:8000/

## Структура проекта
- `my_shop/` - основная конфигурация проекта
- `shop/` - приложение магазина
  - `views.py` - контроллеры страниц
  - `urls.py` - маршрутизация

- `templates/` - HTML шаблоны (будут добавлены позже)
- контрольные вопросы(лр 17):

1. **Поля модели "Товар"**: name (CharField), description (TextField), price (DecimalField), category (ForeignKey), manufacturer (ForeignKey), image (ImageField), created_at (DateTimeField)

2. **Параметр on_delete**: CASCADE - удаление связанных объектов, PROTECT - запрет удаления, SET_NULL - установка NULL

3. **Метод __str__()** - возвращает название категории

4. **MinValueValidator** - для поля price, чтобы цена была положительной

5. **ForeignKey от товара к производителю**. При удалении производителя можно настроить каскадное удаление или защиту

6. **Product.objects.filter(category__name='Электроника')**

7. **order_by('-price')**

8. **Объект Q** - для сложных запросов с OR, применяется с icontains для поиска по названию или описанию

9. **Paginator(products, 10)** с передачей номера страницы через GET-запрос

10. **get_object_or_404(Product, id=id)**

11. **OneToOneField** - связь один к одному

12. **PositiveIntegerField** - только положительные числа

13. **sum(item.product.price * item.count for item in elements)**

14. **Удаляются автоматически** благодаря CASCADE в related_name

15. **Метод get_total_price()** возвращает product.price * count

16. **Поля модели "Товар"**: name (CharField), price (DecimalField), category (ForeignKey), manufacturer (ForeignKey)

17. **on_delete=CASCADE** - удаление связанных объектов, on_delete=PROTECT - защита от удаления

18. **Метод __str__()** - возвращает название категории

19. **MinValueValidator** для price, чтобы цена была положительной

20. **ForeignKey от товара к производителю**. При удалении производителя товары удаляются или защищены

21. **Product.objects.filter(category__name='Электроника')**

22. **order_by('-price')**

23. **Объект Q** - для условий OR в фильтрации

24. **Paginator** с параметром 10 записей на страницу

25. **get_object_or_404()**

26. **OneToOneField к User**

27. **PositiveIntegerField** - только целые положительные числа

28. **Суммированием цены каждого элемента**

29. **Удаляются автоматически** из-за CASCADE

