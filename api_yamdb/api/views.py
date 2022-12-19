from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters,
                            mixins,
                            viewsets,
                            status)
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .permissions import IsAdminOrSuperUser, IsAdminOrSuperUserOrReadOnly

from api.serializers import (CategorySerializer,
                             GenreSerializer,
                             TitleListSerializer,
                             TitleRetrieveSerializer,
                             TitlePostPatchSerializer,
                             UserSerializer,
                             TokenAccessSerializer,
                             )

from reviews.models import Category, Genre, GenreTitle, Title, User


# Система подтверждения через e-mail
@api_view(['POST'])
@permission_classes([AllowAny])
def send_confirmation_code(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    serializer.save(email=email, username=username)
    user = get_object_or_404(User, email=email, username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Confirmation code for getting token',
        f'Confirmation code: {confirmation_code}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    data = {'email': email, 'username': username}
    return Response(data)


# Работа с токеном
@api_view(["POST"])
@permission_classes([AllowAny])
def token_access(request):
    serializer = TokenAccessSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        token = RefreshToken.for_user(user)
        return Response({'token': str(token)})
    return Response(status=status.HTTP_400_BAD_REQUEST)


# Работа с юзерами
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('pk')
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperUser,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('=username',)

    @action(
        methods=["get", "patch"],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        if request.method == "GET":
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    permission_classes = [IsAdminOrSuperUserOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category',
                        'name',
                        'year',
                        'genre'
                        )
    filterset_class = TitleFilter

    def get_queryset(self):
        queryset = Title.objects.all()
        slug = self.request.query_params.get('slug')
        # if slug is not None:
        #     queryset = queryset.filter(genre__slug=slug)
        # return queryset
        if slug is not None:
            slug = self.request.query_params.get('slug')
            # берём из жанров только те, у которых соответсвующий слаг
            querysetG = Genre.objects.filter(slug=slug).values('id')
            # вытаскиваем список id результатов фильтрации (столбик) <<<<<<<<<<<<< реализовано неверно
            g_id = querysetG['id']
            # в промежуточной таблице берём только те строки, в которых id жанра соответсвует прошлому шагу
            querysetGT = GenreTitle.objects.filter(genre_id__in=g_id).values()
            # из этих строк забираем id татлов (столбик) <<<<<<<<<<<<< реализовано неверно
            t_id = querysetGT['title_id']
            # фильтруем titles по id тайтлов
            new_queryset = queryset.filter(genre__title_id__in=t_id)
            return new_queryset
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return TitleListSerializer
        if self.action == 'retrieve':
            return TitleRetrieveSerializer
        return TitlePostPatchSerializer
