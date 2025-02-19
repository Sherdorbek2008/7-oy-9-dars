from django.urls import path
from .views import *

urlpatterns = [
    path("", Index.as_view(), name='home'),
    path('shop/', Products.as_view(), name='shop'),
    path('shop/wishlist', Wishlist.as_view(), name='wishlist'),
    path('shop/about', About.as_view(), name='about'),
    path('shop/<slug:departament_slug>/', Products.as_view(), name='shop_by_departament'),
]
