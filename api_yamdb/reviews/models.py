from django.core.validators import MaxLengthValidator, validate_slug
from django.db import models


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
        return self.name  # slug??


class Genre(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Жанр',
                            unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name  # slug??


class Title(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Название',
                            unique=True)
    year = models.IntegerField(blank=True,
                               null=True,
                               verbose_name='Год выпуска')

    # TBA by another contributor (field type: ForeignKey)
    # ---------------------------------------------------
    rating = models.FloatField(blank=True,
                               null=True)
    # ---------------------------------------------------

    description = models.CharField(max_length=200,
                                   verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre,
        # этот параметр похоже не предусмотрен
        #on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Жанр',
        null=True
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
