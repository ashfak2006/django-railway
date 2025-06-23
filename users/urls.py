from django.urls import path
from . import views
urlpatterns = [
    path('',views.show_page,name='show_page'),
    path('register/',views.register_page,name='register_page'),
    path('logout/',views.user_logout,name='logout'),
    path('about/',views.show_about,name='about'),
    path('account/',views.show_account,name='account'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('add_adress/',views.add_adress,name='add_adress'),
    path('delete_adress/',views.delete_adress,name='delete_adress'),
    path('change_password/',views.change_password,name='change_password'),
    path('order_details/<order_number>/',views.show_order_details,name='order_details'),
]