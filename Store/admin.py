from django.contrib import admin
from .models import Product , Category , CartItem ,Order, OrderItem , ArchivedOrder,ArchivedOrderItems

class ProductAdmin(admin.ModelAdmin):

    search_fields = ['name', 'description']  
    list_display = ['name','unit_price','inventory','discount']  
    list_filter = ['categories','rating_rv','color','discount'] 


admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):  
    list_display = ['title']  
    list_filter = ['title']  

admin.site.register(Category, CategoryAdmin)

# class CartItemAdmin(admin.ModelAdmin):
#     search_fields = ['product__name']  
#     list_display = ['product', 'customer', 'quantity']  
#     list_filter = ['customer', 'product__category']  

admin.site.register(CartItem)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['placed_at', 'customer', 'status', 'total_amount']
    list_filter = ['status']
    search_fields = ['customer__email', 'tracking_number']
    readonly_fields = ['tracking_number']


admin.site.register(Order, OrderAdmin)


class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity']
    list_filter = ['order']
    search_fields = ['order__tracking_number', 'product__name']

admin.site.register(OrderItem, OrderItemsAdmin)

class ArchivedOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'placed_at', 'total_amount']
    list_filter = ['status', 'placed_at']
    search_fields = ['id', 'customer__email']

admin.site.register(ArchivedOrder, ArchivedOrderAdmin)
# admin.site.register(ArchivedOrder)
admin.site.register(ArchivedOrderItems)







