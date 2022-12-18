from rest_framework import (filters,
                            mixins,
                            viewsets, status)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response

from .permissions import IsAdminOrSuperUser, IsAdminOrSuperUserOrReadOnly

from api.serializers import (CategorySerializer,
                             GenreSerializer,
                             TitleSerializer,
                             UserSerializer)

from reviews.models import Category, Genre, Title


# Система подтверждения через e-mail
def send_confirmation_code(request):
    serializer = UserSerializer(data=request.data)
    pass


# Работа с токеном
def token_access(request):
    pass


# Работа с юзерами
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    pass

    def me(self):
        pass


# От этого вьюсета надо наследовать вьюсеты для категорий и жанров
class ListAddDeleteViewSet(mixins.ListModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListAddDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrSuperUserOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'



class GenreViewSet(ListAddDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrSuperUserOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrSuperUserOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category',
                        'genre',
                        'name',
                        'year'
                        )
