from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from photos.api import PhotoViewSet

#API Router
router = DefaultRouter()
router.register(r'photos', PhotoViewSet)

urlpatterns = [
    url(r'1.0/', include(router.urls)),
]