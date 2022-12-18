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
        # fields = '__all__'
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        # fields = '__all__'
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, required=False)
    # genre = serializers.SlugRelatedField(required=True,
    #                                      many=True,
    #                                      slug_field='slug',
    #                                      queryset=Genre.objects.all()
    #                                      )
    category = CategorySerializer(many=False, required=True)
    # category = serializers.SlugRelatedField(required=True,
    #                                         slug_field='slug',
    #                                         queryset=Category.objects.all()
    #                                         )


    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        year_now = dt.date.today().year
        if not (value < year_now):
            raise serializers.ValidationError('Проверьте год публикации/выхода!')
        return value
