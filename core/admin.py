from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff','is_member_club','date_joined')
    list_filter = ('is_active', 'is_staff','is_member_club','city')
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email',)
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'birth_date','profile_image')}),
        ('Contact Info', {'fields': ('phone_number', 'city', 'address', 'postal_code')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Membership', {'fields': ('is_student', 'is_member_club', 'member_club_reduction')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # def get_fields(self, request, obj=None):
    #     fields = super().get_fields(request, obj=obj)
    #     if obj and obj.is_member_club:
    #         fields += ('member_club_reduction_limit',)  # Add the calculated field when is_member_club is True
    #     return fields

    # def member_club_reduction_limit(self, obj):
    #     # Multiply the price by 170
    #     return obj.member_club_reduction * 170

    # member_club_reduction_limit.short_description = ' Price DZ'



admin.site.register(CustomUser, CustomUserAdmin)