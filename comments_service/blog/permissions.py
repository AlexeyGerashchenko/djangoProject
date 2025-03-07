from rest_framework import permissions
from django.contrib.auth.models import User


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее только владельцам объекта редактировать его.
    """
    
    def has_object_permission(self, request, view, obj):
        # Разрешения на чтение разрешены для любого запроса
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Разрешения на запись только владельцу объекта
        # Проверяем, является ли объект пользователем
        if isinstance(obj, User):
            return obj == request.user
        
        # Проверяем, есть ли у объекта атрибут 'author' или 'user'
        if hasattr(obj, 'author'):
            return obj.author == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False 