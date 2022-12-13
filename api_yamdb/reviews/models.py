from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Категория',
                            unique=True)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Жанр',
                            unique=True)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Название',
                            unique=True)
    year = models.DateTimeField(blank=True,
                                null=True)

    # TBA by another contributor (field type: ForeignKey)
    # ---------------------------------------------------
    rating = models.FloatField(blank=True,
                               null=True)
    # ---------------------------------------------------

    description = models.CharField(max_length=200,
                                   verbose_name='Описание')
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Категория'
    )
