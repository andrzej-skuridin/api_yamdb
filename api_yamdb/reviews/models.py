from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, validate_slug
from django.core.validators import MaxValueValidator, MinValueValidator

class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLE_CHOICES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
    ]

    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(
        'Информация о пользователе',
        help_text='Введите краткую информацию о себе',
        blank=True,
        null=True,
    )
    role = models.CharField(max_length=9, choices=ROLE_CHOICES, default=USER)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        self.is_active = True
        if self.role == self.ADMIN:
            self.is_staff = True
        super(User, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Категория',
                            unique=True,
                            validators=[MaxLengthValidator(limit_value=256)]
                            )
    slug = models.SlugField(unique=True,
                            max_length=50,
                            validators=[validate_slug,
                                        MaxLengthValidator(limit_value=50)
                                        ]
                            )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Жанр',
                            unique=True,
                            validators=[MaxLengthValidator(limit_value=256)]
                            )
    slug = models.SlugField(unique=True,
                            max_length=50,
                            validators=[validate_slug,
                                        MaxLengthValidator(limit_value=50)
                                        ]
                            )

    def __str__(self):
        return self.name  # slug??


class Title(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название',
                            unique=True,
                            validators=[MaxLengthValidator(limit_value=256)]
                            )
    year = models.IntegerField(blank=True,
                               null=True,
                               verbose_name='Год выпуска')

    # TBA by another contributor (field type: ForeignKey)
    # ---------------------------------------------------
    rating = models.SmallIntegerField(blank=True, null=True)
    # ---------------------------------------------------

    description = models.CharField(max_length=200,
                                   verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre,
        # этот параметр похоже не предусмотрен
        # null=True
        #on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    score = models.SmallIntegerField(
        validators=[MaxValueValidator(10),
                    MinValueValidator(1)])
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]
