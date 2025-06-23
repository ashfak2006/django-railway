from django.contrib import admin
from .models import Order,Order_item,Discount,Shipping,payment
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
   
    list_display = ('order_number','grand_total', 'status', 'order_date', 'updated_at')
    list_filter = ('status','order_date', 'updated_at','processed_at')

class shippingAdmin(admin.ModelAdmin):
    list_display = ('tracking_number','shipping_method', 'status', 'order_date', 'shipped_at','cost')
    list_filter = ('status','shipping_method', 'updated_at','shipped_at','delivered_at')


admin.site.register(Order,OrderAdmin)
admin.site.register(Order_item)
admin.site.register(Discount)
admin.site.register(Shipping)
admin.site.register(payment)