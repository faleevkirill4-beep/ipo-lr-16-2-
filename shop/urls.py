from django.urls import path 
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('shop_info/', views.shop_info, name='shop_info'),

    #для функций представлений
    path('catalog/',views.product_list,name='product_list'),
    path('categories/',views.category_list,name='category_list'),
    path('basket/',views.basket,name='basket'),
    path('catalog/<int:pk>/', views.product_detail, name ='product_detail'),
    path('basket/add/<int:product_id>/', views.add, name ='add'),
    path('basket/update/<int:item_id>/', views.update_basket_quantity, name ='update_basket_quantity'),
    path('basket/remove/<int:item_id>/', views.remove_from_basket, name ='remove_from_basket'),
    path('basket/checkout/', views.checkout, name = 'checkout')
]