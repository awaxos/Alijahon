from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import Model, DateTimeField, CharField, ImageField, SlugField, TextField, FloatField, ForeignKey, \
    CASCADE, IntegerField, TextChoices
from django.utils.functional import cached_property
from django.utils.text import slugify


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        user = self.create_user(phone_number, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        # user.save()
        return user


class User(AbstractUser):
    class Role(TextChoices):
        ADMIN = "admin", 'Admin'
        OPERATOR = "operator", 'Operator'
        MANAGER = "manager", 'Manager'
        DRIVER = "driver", 'Driver'
        USER = "user", 'User'

    username = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    role = CharField(max_length=50, choices=Role.choices, default=Role.USER)
    phone_number = CharField(max_length=12, unique=True)
    district = ForeignKey('apps.District', CASCADE, related_name='users', null=True)

    @property
    def wishlist_all(self):
        return self.wishlists.values_list('product_id', flat=True)


class Region(Model):
    name = CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class District(Model):
    name = CharField(max_length=255, unique=True)
    region = ForeignKey('apps.Region', CASCADE, related_name='districts')

    def __str__(self):
        return self.name


class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_et = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseSlugModel(Model):
    name = CharField(max_length=255)
    slug = SlugField(unique=True)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        while self.__class__.objects.filter(slug=self.slug).exists():
            self.slug += '-1'
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name


class Category(BaseSlugModel):
    image = ImageField(upload_to='images/')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


# class SiteSettings(Model):
#     name = CharField(max_length=255)

class Product(BaseSlugModel, BaseModel):
    description = TextField()
    price = FloatField()
    quantity = IntegerField()
    for_stream_price = FloatField(default=1000)
    category = ForeignKey('apps.Category', CASCADE, to_field='slug', related_name='products')

    @property
    def first_image(self):
        return self.images.first()



    def __str__(self):
        return self.name


class ProductImage(Model):
    image = ImageField(upload_to='products/')
    product = ForeignKey('apps.Product', CASCADE, related_name='images')




class Order(BaseModel):
    product = ForeignKey('apps.Product', CASCADE, related_name='orders')
    quantity = IntegerField(default=1)
    user = ForeignKey('apps.User', CASCADE, related_name='orders')
    full_name = CharField(max_length=255)
    phone_number = CharField(max_length=20)


class WishList(BaseModel):
    product = ForeignKey('apps.Product', CASCADE, related_name='wishlists', to_field='slug')
    user = ForeignKey('apps.User', CASCADE, related_name='wishlists')