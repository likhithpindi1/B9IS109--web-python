from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    first_name = models.CharField(max_length=200, unique=False, null=True)
    last_name = models.CharField(max_length=200, null=True)
    phone_no = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=200, unique=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class products_names(models.Model):
    item_name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    item_img = models.ImageField(upload_to="img/%Y/%m/%d", blank=True)

    def __str__(self):
        return self.item_name


class Cart(models.Model):
    product = models.ForeignKey(products_names, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantaty = models.IntegerField(default=0)

    def __str__(self):
        return self.product.item_name

    @property
    def amount(self):
        return self.product.price * self.quantaty
