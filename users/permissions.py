# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):


    def has_permission(self, request, view):
        from users.api import UserViewSet
        """Define si el usuario registrado tiene derecho a hacer una accion"""
        if view.action == 'create':
            return True
        elif request.user.is_superuser:
            return True
        elif view.action in ['retrieve', 'update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        """Define si el usuario registrado en request.user tiene derecho a hacer una accion sobre el objeto obj"""
        return request.user.is_superuser or request.user == obj
