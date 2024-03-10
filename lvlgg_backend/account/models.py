from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(
        self,
        email,
        username,
        firstname,
        lastname,
        password=None,
        **extra_fields,
    ):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The username field must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            firstname=firstname,
            lastname=lastname,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        username,
        firstname,
        lastname,
        password=None,
        **extra_fields,
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(
            email=email,
            username=username,
            password=password,
            firstname=firstname,
            lastname=lastname,
            **extra_fields,
        )


class Client(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True, null=True)
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    friends = models.ManyToManyField("self", symmetrical=False, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["firstname", "lastname", "email", "password"]

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
