from django.urls import path
from . import views
urlpatterns = [
    path('products_list/<catagoris>',views.product_list,name='products_list'),
    path('products_list/',views.product_list1,name='products_list1'),
    # path('product_details/',views.product_details,name='product_details'),
    path('product_details/<pk>/',views.product_details,name='product_details'),
    path('add_review/',views.add_review,name='add_review'),
    path('product_search/', views.product_search, name='product_search'),
   
]