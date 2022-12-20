from django.urls import include, path
from rest_framework import routers

from api.views import (CategoryViewSet,
                       GenreViewSet,
                       TitleViewSet,
                       ReviewViewSet,
                       token_access,
                       send_confirmation_code,
                       UserViewSet
                       )

v1_router = routers.DefaultRouter()
v1_router.register('users', UserViewSet)
v1_router.register(prefix='titles',
                   basename='title',
                   viewset=TitleViewSet)
v1_router.register(prefix='categories',
                   basename='categories',
                   viewset=CategoryViewSet)
v1_router.register(prefix='genres',
                   basename='genres',
                   viewset=GenreViewSet)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/token/', token_access, name='token'),
    path('v1/auth/signup/', send_confirmation_code, name='signup'),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
]
