from django.urls import path
from . import views
urlpatterns = [
    path('cart/',views.show_cart,name='cart'),
    path('cart_add/',views.add_to_cart,name='add_to_cart'),
    path('remove_item/<pk>',views.remove_item_from_cart,name='remove_item'),
    path('check_out/',views.check_out,name='check_out'),
    path('apply_discount/',views.apply_discount,name='apply_discount'),
    path('remove_discount/',views.remove_discount,name='remove_discount'),
    path('palce_order/',views.palce_order,name='palce_order'),
    path('cancel_order/<order_number>',views.cancel_order,name='cancel_order'),
    
]