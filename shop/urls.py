from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('shop_info/', views.shop_info, name='shop_info'),

    #для функций представлений
    path('products/',views.product_list,name='product_list'),
    path('categories/',views.category_list,name='category_list'),
    path('bascet/',views.bascet,name='bascet'),
]