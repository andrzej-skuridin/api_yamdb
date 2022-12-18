import datetime as dt

from django.core.exceptions import ValidationError
from rest_framework import serializers

from reviews.models import Category, Genre, Title, User, GenreTitle


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


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, required=False)
    category = CategorySerializer(many=False, required=True)

    class Meta:
        model = Title
        fields = '__all__'


class OverrideTitleSerializer(serializers.ModelSerializer):
    # https://practicum.yandex.ru/learn/backend-developer/courses/8a4693f6-fa0e-4ab0-babd-a13453ad99c0/sprints/73398/topics/eb215b6a-1a94-46e8-b1ed-6f4da1956b01/lessons/062f1640-6723-4c8b-95aa-50c620474275/
    # Операции записи с вложенными сериализаторами

    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='genre__slug',
        queryset=Title.objects.all()
    )
    category = serializers.SlugRelatedField(
        many=False,
        slug_field='category__slug',
        queryset=Title.objects.all()
    )

    class Meta:
        model = Title
        fields = ('name',
                  'year',
                  'description',
                  'genre',
                  'category'
                  )

    def validate_year(self, value):
        year_now = dt.date.today().year
        if not (value < (year_now + 1)):
            raise serializers.ValidationError('Проверьте год публикации/выхода!')
        return value

    def create(self, validated_data):
        genre = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for g in genre:
            current_g, status = Genre.objects.get_or_create(
                **g)
            GenreTitle.objects.create(
                g=current_g, title=title)
        return title
