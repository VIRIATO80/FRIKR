from django.conf.urls import url, include
from users.api import UserViewSet
from rest_framework.routers import DefaultRouter

# API Router
router = DefaultRouter()
router.register(r'users', UserViewSet, base_name='users')

urlpatterns = [
    # API URLs
    url(r'1.0/', include(router.urls)),
]
