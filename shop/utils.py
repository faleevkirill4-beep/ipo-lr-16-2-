import openpyxl
from openpyxl.styles import Font, Alignment
from io import BytesIO
from datetime import datetime

def create_excel_receipt(user, items, total_price):
    """Создание Excel чека
    
    Аргументы:
    - user: объект пользователя Django
    - items: QuerySet объектов BasketItem
    - total_price: общая сумма заказа
    """
    
    # Создаем Excel файл
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Чек заказа"
    
    # Заголовок
    ws['A1'] = 'ЧЕК ЗАКАЗА'
    ws['A1'].font = Font(size=16, bold=True)
    ws['A1'].alignment = Alignment(horizontal='center')
    ws.merge_cells('A1:D1')
    
    # Информация о заказе
    ws['A3'] = f'Дата: {datetime.now().strftime("%d.%m.%Y %H:%M")}'
    ws['A4'] = f'Покупатель: {user.username}'
    ws['A5'] = f'Email: {user.email}'
    
    # Заголовки таблицы
    ws['A7'] = 'Товар'
    ws['B7'] = 'Цена'
    ws['C7'] = 'Кол-во'
    ws['D7'] = 'Сумма'
    
    for cell in ['A7', 'B7', 'C7', 'D7']:
        ws[cell].font = Font(bold=True)
        ws[cell].alignment = Alignment(horizontal='center')
    
    # Заполняем товары
    row = 8
    for item in items:
        ws[f'A{row}'] = item.product.name
        ws[f'B{row}'] = f'{item.product.price}BYN'
        ws[f'C{row}'] = item.count
        ws[f'D{row}'] = f'{item.product.price * item.count} BYN'
        
        ws[f'B{row}'].alignment = Alignment(horizontal='right')
        ws[f'C{row}'].alignment = Alignment(horizontal='center')
        ws[f'D{row}'].alignment = Alignment(horizontal='right')
        row += 1
    
    # Итог
    row += 1
    ws[f'C{row}'] = 'ИТОГО:'
    ws[f'C{row}'].font = Font(bold=True)
    ws[f'C{row}'].alignment = Alignment(horizontal='right')
    
    ws[f'D{row}'] = f'{total_price} ₽'
    ws[f'D{row}'].font = Font(bold=True)
    ws[f'D{row}'].alignment = Alignment(horizontal='right')
    
    # Настраиваем ширину колонок
    ws.column_dimensions['A'].width = 35
    ws.column_dimensions['B'].width = 12
    ws.column_dimensions['C'].width = 10
    ws.column_dimensions['D'].width = 15
    
    # Сохраняем в память
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    return output