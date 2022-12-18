import re
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Genre, Title, Review


class UserSerializer(serializers.ModelSerializer):
    pass


class TokenAccessSerializer(serializers.Serializer):
    pass


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        if len(value) > 256:
            raise serializers.ValidationError(
                'Слишком длинное название!'
            )
        return value

    def validate_slug(self, value):
        if len(value) > 50:
            raise serializers.ValidationError(
                'Слишком длинный slug!'
            )
        if re.match(pattern='[-a-zA-Z0-9_]+$', string=value) is None:
            raise serializers.ValidationError(
                'В поле slug некорректные данные!'
            )
        return value


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

    def validate_name(self, value):
        if len(value) > 256:
            raise serializers.ValidationError(
                'Слишком длинное название!'
            )
        return value

    def validate_slug(self, value):
        if len(value) > 50:
            raise serializers.ValidationError(
                'Слишком длинный slug!'
            )
        if re.match(pattern='[-a-zA-Z0-9_]+$', string=value) is None:
            raise serializers.ValidationError(
                'В поле slug некорректные данные!'
            )
        return value


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(required=True,
                                        many=True,
                                        slug_field='slug',
                                        queryset=Genre.objects.all()
                                        )
    category = serializers.SlugRelatedField(required=True,
                                            slug_field='slug',
                                            queryset=Category.objects.all()
                                            )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def validate_name(self, value):
        if len(value) > 256:
            raise serializers.ValidationError(
                'Слишком длинное название!'
            )
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
