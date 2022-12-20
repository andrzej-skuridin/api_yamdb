import datetime as dt
from django.db.models import Avg
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Genre, Title, Review

from django.core.exceptions import ValidationError
from rest_framework import serializers

from reviews.models import Category, Genre, Title, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(
                'Нельзя использовать зарезвированное имя "me".')
        return value


class TokenAccessSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleListSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True, required=False)
    category = CategorySerializer(many=False, required=True)

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        year_now = dt.date.today().year
        if not (value < (year_now + 1)):
            raise serializers.ValidationError('Проверьте год публикации/выхода!')
        return value

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score'))['score__avg']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'author', 'title', 'text', 'score', 'pub_date')
        read_only_fields = ('author', 'title', 'pub_date', 'id')

class TitleRetrieveSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, required=False)
    category = CategorySerializer(many=False, required=True)
    pagination_class = None

    class Meta:
        model = Title
        fields = '__all__'


class TitlePostPatchSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(required=True,
                                         many=True,
                                         slug_field='slug',
                                         queryset=Genre.objects.all()
                                         )
    category = serializers.SlugRelatedField(required=True,
                                            slug_field='slug',
                                            queryset=Category.objects.all()
                                            )

    class Meta:
        model = Title
        fields = '__all__'
