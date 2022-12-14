from django.contrib.auth.models import AbstractUser
from django.db import models


CHOICES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
)


class User(AbstractUser):
    email = models.EmailField(
        'email',
        unique=True,
        max_length=254,
    )

    first_name = models.CharField(
        max_length=150,
        blank=True,
    )

    role = models.CharField(
        max_length=9,
        choices=CHOICES,
        default='user',
    )
