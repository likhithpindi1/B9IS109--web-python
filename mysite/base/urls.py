
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = [
    path('', views.home,name='home'),
    path('shop/', views.shop,name='shop'),
    path('register/', views.register,name='register'),
    path('login/', views.login_page,name='login'),
    path('logout/', views.logout_page,name='logout'),
    path('search/', views.getSearchProducts, name='search_products'),
    
    path('cart/', views.cart_page, name='cart_page'),
    
    path('add To Cart/', views.CartAddProduct, name='add_to_cart'),
    
    path('Delete Item/<str:pk>/', views.deleteItem, name='delete_item'),
    
    path('Order Placed/', views.orderPlaced, name='order_placed'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
