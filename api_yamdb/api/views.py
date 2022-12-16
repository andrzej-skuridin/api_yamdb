from rest_framework import (filters,
                            mixins,
                            viewsets)

from .permissions import AdminOrReadOnly

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
    # permission_classes = [AdminOrReadOnly]
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('name',)


class GenreViewSet(ListAddDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = [AdminOrReadOnly]
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('name',)



class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # permission_classes = [AdminOrReadOnly]
    # filter_backends = (filters.BaseFilterBackend,)
    # filterset_fields = ('category',
    #                     'genre',
    #                     'name',
    #                     'year'
    #                     )

