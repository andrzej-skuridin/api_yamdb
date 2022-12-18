import re
import datetime as dt

from rest_framework import serializers

from reviews.models import Category, Genre, Title


class UserSerializer(serializers.ModelSerializer):
    pass


class TokenAccessSerializer(serializers.Serializer):
    pass


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

    def validate_year(self, value):
        year_now = dt.date.today().year
        if not (value < (year_now + 1)):
            raise serializers.ValidationError('Проверьте год публикации/выхода!')
        return value
