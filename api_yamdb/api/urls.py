from django.urls import include, path
from rest_framework import routers

from api.views import (CategoryViewSet,
                       GenreViewSet,
                       TitleViewSet)

v1_router = routers.DefaultRouter()
v1_router.register(prefix='titles',
                   basename='title',
                   viewset=TitleViewSet)
v1_router.register(prefix='categories',
                   basename='categories',
                   viewset=CategoryViewSet)
v1_router.register(prefix='genres',
                   basename='genres',
                   viewset=GenreViewSet)


urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
