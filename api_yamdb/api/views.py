from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
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


from .permissions import IsAdminOrSuperUser, IsAdminOrSuperUserOrReadOnly

from api.serializers import (CategorySerializer,
                             GenreSerializer,
                             TitleSerializer,
    # TitlePostPatchSerializer,
                             UserSerializer,
                             TokenAccessSerializer, OverrideTitleSerializer)

from reviews.models import Category, Genre, Title, User


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

    # serializer_class = TitleSerializer
    serializer_class = OverrideTitleSerializer

    # permission_classes = [IsAdminOrSuperUserOrReadOnly]
    permission_classes = [AllowAny]

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category',
                        'genre',
                        'name',
                        'year'
                        )

    # def get_serializer_class(self):
    #     # Если запрошенное действие (action) — получение списка объектов ('list')
    #     actions = ('retrieve',
    #                'update',
    #                'partial_update')
    #     if self.action in actions:
    #         return TitlePostPatchSerializer
    #     return TitleSerializer
