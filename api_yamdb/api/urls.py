from django.urls import include, path
from rest_framework import routers

from api.views import (CategoryViewSet,
                       GenreViewSet,
                       TitleViewSet,
                       token_access,
                       send_confirmation_code)

v1_router = routers.DefaultRouter()
#v1_router = routers.SimpleRouter()
v1_router.register(prefix='categories',
                   viewset=CategoryViewSet,
                   basename='categories')
v1_router.register(prefix='genres',
                   viewset=GenreViewSet,
                   basename='genres')
v1_router.register(prefix='titles',
                   viewset=TitleViewSet,
                   basename='titles')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/token/', token_access, name='token'),
    path('v1/auth/signup/', send_confirmation_code, name='signup'),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
]
