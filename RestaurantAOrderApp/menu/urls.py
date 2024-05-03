from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('breakfast/', views.breakfast, name='breakfast'),
    path('lunch/', views.lunch, name='lunch'),
    path('drinks/', views.drinks, name='drinks'),
    path('dessert/', views.dessert, name='dessert'),
    path('sides/', views.sides, name='sides'),
    path('cart/<int:table_number>/', views.cart, name='cart'),
    path('delete_item/<int:table_number>/<int:item_id>/', views.delete_item, name='delete_item'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('make_order/<int:table_number>/', views.make_order, name='make_order'),
]
