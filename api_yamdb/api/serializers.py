import re

from rest_framework import serializers

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

    def validate(self, data):
        if len(data['name']) > 256:
            raise serializers.ValidationError(
                'Слишком длинное название!'
            )
        if len(data['slug']) > 50:
            raise serializers.ValidationError(
                'Слишком длинный slug!'
            )
        if re.match(pattern='[-a-zA-Z0-9_]+$', string=data['slug']) is None:
            raise serializers.ValidationError(
                'В поле slug некорректные данные!'
            )
        return data


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, required=True)
    #genre = serializers.SlugRelatedField(required=True,
    #                                     many=True,
    #                                     slug_field='slug',
    #                                     queryset=Genre.objects.all()
    #                                     )
    category = serializers.SlugRelatedField(required=True,
                                            slug_field='slug',
                                            queryset=Category.objects.all()
                                            )

    class Meta:
        model = Title
        fields = '__all__'
