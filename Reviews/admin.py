from django.contrib import admin
from .models import Review
# Register your models here.
# admin.site.register(Review)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'rating', 'content']
    list_filter = ['product', 'user', 'rating']
    search_fields = ['product__name', 'user__email']

admin.site.register(Review, ReviewAdmin)