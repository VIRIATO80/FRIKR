#-*- coding: utf-8 -*-
from rest_framework.filters import SearchFilter, OrderingFilter

from photos.models import Photo
from photos.views import PhotosQueryset
from photos.serializers import PhotoSerializer, PhotoListSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

class PhotoViewSet(PhotosQueryset, ModelViewSet):

    queryset = Photo.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (SearchFilter, OrderingFilter)
    ordering_fields = ('name', 'owner')
    search_fields = ('name', 'description')

    def get_queryset(self):
        return self.get_photo_queryset(self.request)

    def get_serializer_class(self):
        if self.action == 'list':
            return PhotoListSerializer
        else:
            return PhotoSerializer

    def perform_create(self, serializer):
        # Asigna de manera automática la autoría de la nueva foto
        serializer.save(owner=self.request.user)


"""
class PhotoListAPI(PhotosQueryset, ListCreateAPIView):
    queryset = Photo.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        return PhotoSerializer if self.request.method == 'POST' else PhotoListSerializer

    def get_queryset(self):
        return self.get_photo_queryset(self.request)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PhotoDetailAPI(PhotosQueryset, RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return self.get_photo_queryset(self.request)
"""