from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField(
        blank = True,
        null = True
    )

    def __str__(self):
        return self.name 


   
class Manufacturer(models.Model):
    name = models.CharField(
        max_length=100,
    )
    country = models.CharField(
        max_length=100,
    )
    description = models.TextField(
        null=True,
        blank = True
    )

    def __str__(self):
        return self.name 
    


class Product(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField()
    product_photo = models.ImageField(
        upload_to='products/',
        blank = True,
        null=True,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinLengthValidator(0)
        ]
    )
    count = models.IntegerField(
        validators=[
            MinLengthValidator(0)
        ]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Категория",
        help_text="выберите категорию товара" 
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Производитель",
        help_text="Выберите производителя товара",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name
 

class Bascet(models.Model):
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        related_name='bascet',
        verbose_name="Пользователь",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"
    #сделать метод для высчитывания общей стоймости всех элементов корзины
    """ def total_coast(self):
        price_elem = 0.0
        for elem in self.elements.all():
            price_elem+=elem.Price_element()
        return price_elem
    """
class Element_bascet(models.Model):
    bascet = models.ForeignKey(
        Bascet,
        on_delete=models.CASCADE,
        related_name ='elements',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name ='in_bascet',
    )
    count = models.PositiveIntegerField()
    

    def __str__(self):
        return f"{self.product.name} - {self.count} шт."
    
    def Price_element(self):
        return self.product.price * self.count
        
    

