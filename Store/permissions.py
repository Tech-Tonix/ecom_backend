from rest_framework import permissions
from .models import Order

class CanModifyOrder(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE', 'PUT', 'PATCH']:
            return obj.status == Order.STATUS_PENDING
        return True


