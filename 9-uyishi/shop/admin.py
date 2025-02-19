from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

admin.site.site_header = "Vegefoods"


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name')
    list_display_links = ('id', 'username')


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Departamenent)
class DepartamentAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug", "get_image")
    list_display_links = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [CategoryInline]

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" />')
        return "No Image"

    get_image.short_description = "Image Preview"


class ProductPhotoInline(admin.TabularInline):
    model = ProductPhoto
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'slug', 'price', 'get_image', 'description', 'in_stock', 'sold', 'rating', 'type_product',
        'discount', 'size', 'category'
    )
    list_display_links = ('id', 'name')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductPhotoInline]

    def get_image(self, product):
        photos = product.images.all()
        if photos.exists():
            return mark_safe(f'<img src="{photos[0].photo.url}" width="100" />')
        return "No Image"

    get_image.short_description = "Image Preview"
