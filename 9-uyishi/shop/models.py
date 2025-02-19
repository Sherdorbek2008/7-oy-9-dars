from django.db import models
from django.contrib.auth.models import AbstractUser


# User model
class MyUser(AbstractUser):
    phone = models.CharField(max_length=13, null=True, blank=True)
    photo = models.ImageField(upload_to='users/photo', null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ['id']


class Departamenent(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Bo'limni Nomi")
    slug = models.SlugField(max_length=150, unique=True)
    image = models.ImageField(upload_to="departaments/images/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Bo'lim"
        verbose_name_plural = "Bo'limlar"
        ordering = ['id']


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Kategoriya Nomi')
    slug = models.SlugField(max_length=150, unique=True)
    departament = models.ForeignKey(Departamenent, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['id']


TYPE_PRODUCT = (
    ("t", "Tonnes"),
    ("kg", "Kilogrammes"),
    ("l", "Litres"),
    ("ml", "Millilitres"),
)

SIZE_TYPES = (
    ("sm", "Small"),
    ("md", "Medium"),
    ("lg", "Large"),
    ("elg", "Extra Large"),
)


class Product(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.IntegerField(default=100)
    sold = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    type_product = models.CharField(max_length=2, choices=TYPE_PRODUCT, default="kg")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    size = models.CharField(max_length=8, choices=SIZE_TYPES, default="sm")
    related = models.ManyToManyField('self', blank=True)
    discount = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.rating < 0 or self.rating > 5:
            raise ValueError("Rating 0 bilan 5 ni oraligida  bolishi kerak.")
        super().save(*args, **kwargs)

    def increment_sold(self, quantity=1):
        if quantity < 0:
            raise ValueError("In_stock musbat son bo'lishi kerak")
        self.sold += quantity
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['id']


class ProductPhoto(models.Model):
    photo = models.ImageField(upload_to='products/photos/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"{self.product.name} - {self.photo.name}"

    class Meta:
        verbose_name = "Mahsulot Rasmi"
        verbose_name_plural = "Mahsulot Rasmlari"
        ordering = ['id']
