from rest_framework import permissions
from .models import Order

# class CanModifyOrder(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in ['DELETE', 'PUT', 'PATCH']:
#             return obj.status == Order.STATUS_PENDING
#         return True

class CanModifyOrderStatus(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'PUT' or request.method == 'DELETE':
            return request.user.is_staff
        return True



