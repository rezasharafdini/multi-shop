from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.html import format_html


class MyUserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        """
        Creates and saves a User with the given phone and password.
        """
        if not phone:
            raise ValueError("Users must have a phone")

        user = self.model(
            phone=phone

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            phone,
            password=password,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    phone = models.CharField(max_length=255,verbose_name='username',unique=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )

    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='user/images',default='user/images/user.png')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone


    def show_image(self):
        return format_html(f'<img src="{self.image.url}" width="50px" height="50px" >')

    show_image.short_description = 'image'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin