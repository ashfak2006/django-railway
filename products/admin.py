from django.contrib import admin
from .models import products, Review, Catogaries

class productsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'price', 'stock', 'stock_status', 'created_at', 'updated_at')
    list_filter = ('stock_status','created_at', 'updated_at')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'rating', 'user', 'created_at', 'updated_at','approved')
    list_filter = ('rating','approved', 'user', 'product','is_verifeid_purchaser')
    search_fields = ('product__title', 'user__username')
admin.site.register(products,productsAdmin)
admin.site.register(Review, ReviewAdmin)  
admin.site.register(Catogaries)
# Register your models here.
