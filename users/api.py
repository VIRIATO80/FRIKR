# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from permissions import UserPermission
from rest_framework.viewsets import ViewSet


class UserViewSet(ViewSet):
    permission_classes = (UserPermission,)

    def list(self, request):
        self.check_permissions(request)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        paginator = PageNumberPagination()
        paginator.paginate_queryset(users, request)
        serializer_user = serializer.data
        return paginator.get_paginated_response(serializer_user)

    def create(self, request):
        self.check_permissions(request)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        self.check_permissions(request)
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk):
        self.check_permissions(request)
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        self.check_permissions(request)
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)