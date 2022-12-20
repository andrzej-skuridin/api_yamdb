import re

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


class RegisterDataSerializer(serializers.Serializer):
    username = serializers.RegexField(
        max_length=150,
        required=True,
        regex=r"^[\w.@+-]+\Z"
    )
    email = serializers.EmailField(
        max_length=254,
        required=True
    )

    def validate_username(self, username):
        if username.lower() == "me":
            raise serializers.ValidationError('Недопустимое имя пользователя')
        return username

    def validate(self, data):
        if User.objects.filter(username=data['username'],
                               email=data['email']).exists():
            return data
        if (User.objects.filter(username=data['username']).exists()
                or User.objects.filter(email=data['email']).exists()):
            raise serializers.ValidationError('Почта или имя уже использовались')
        return data


class TokenAccessSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


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
    # genre = GenreSerializer(many=True, required=True)
    genre = serializers.SlugRelatedField(required=True,
                                         many=True,
                                         slug_field='slug',
                                         queryset=Genre.objects.all()
                                         )
    # category = CategorySerializer(required=True)
    category = serializers.SlugRelatedField(required=True,
                                            slug_field='slug',
                                            queryset=Category.objects.all()
                                            )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_name(self, value):
        if len(value) > 256:
            raise serializers.ValidationError(
                'Слишком длинное название!'
            )
        return value
