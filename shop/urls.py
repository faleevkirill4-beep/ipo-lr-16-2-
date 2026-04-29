from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


router = DefaultRouter()


router.register(r'products',views.ProductViewSet,basename = 'api-product')
router.register(r'categories',views.CategoryViewSet,basename = 'api-category')
router.register(r'manufakturers',views.ManufacturerViewSet,basename = 'api-manufacturer')
router.register(r'basket',views.BasketViewSet, basename='api-basket')
router.register(r'basket-items',views.BasketItemViewSet, basename='api-basket-item')


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
    path('basket/checkout/', views.checkout, name = 'checkout'),
    path('api/',include(router.urls)),

    path('api/basket/add/', views.api_add_to_basket, name='api_add_to_basket'),
    path('api-auth/', include('rest_framework.urls')),  # Логин/логаут в браузере
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # Получение токена

      path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),



]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


