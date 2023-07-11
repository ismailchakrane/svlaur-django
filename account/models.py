import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone


class CustomUserManager(UserManager):
    def _create_user(self, lastname, firstname, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        
        email = self.normalize_email(email)
        user = self.model(lastname=lastname, firstname=firstname, email=email, **extra_fields)
        user.set_password(password)
        user.is_active - True
        user.save(using=self._db)

        return user
    
    def create_user(self, lastname=None, firstname=None, password=None, email=None, **extra_fields):
        extra_fields.setdefault('is_admin', False)
        return self._create_user(lastname, firstname, email, password,  **extra_fields)
    
    def create_adminuser(self, lastname=None, firstname=None, password=None, email=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return self._create_user(lastname, firstname, password, email, **extra_fields)
        

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    last_name = models.CharField(max_length=50,blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    password = models.CharField(max_length=255, blank=False)
    major = models.CharField(max_length=255, blank=False)
    year_of_major = models.CharField(max_length=4, blank=False)
    linkedin_link = models.URLField(blank=True, null=True)
    place_of_work = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    year_of_graduate = models.CharField(max_length=9, blank=True, null=True)
    is_graduate = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
