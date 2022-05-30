from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    USERS_ROLE = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    )
    username = models.CharField(
        "Никнейм", max_length=150, blank=True, unique=True,
    )
    email = models.EmailField(
        "Электронная почта", unique=True, blank=True, max_length=254,
    )
    role = models.CharField(
        "Роль", max_length=30, default=USER, choices=USERS_ROLE,
    )
    bio = models.TextField(
        "Обо мне", max_length=300, blank=True, null=True
    )
    first_name = models.CharField(
        "Имя", max_length=150, blank=True
    )
    last_name = models.CharField(
        "Фамилия", max_length=150, blank=True, null=True
    )


    class Meta(AbstractUser.Meta):
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def is_admin(self):
        return self.is_staff or self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username
