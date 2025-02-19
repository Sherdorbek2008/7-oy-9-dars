import random

from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView

from .models import *


class Index(ListView):
    model = Departamenent
    template_name = 'departamenent_list.html'
    context_object_name = "departments"
    paginate_by = 3
    ordering = ["-name"]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['categories'] = Category.objects.all()
        products = Product.objects.all()
        context['products'] = random.sample(list(products), min(8, len(products))) if products else []
        return context


class Products(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'product_list.html'

    def get_queryset(self):
        departament_slug = self.request.GET.get('departament', None)

        if departament_slug:
            departament = get_object_or_404(Departamenent, slug=departament_slug)
            products = Product.objects.filter(category__departament=departament)
        else:
            products = Product.objects.all()
        if len(products) >= 8:
            product_list = random.sample(list(products), 8)
        else:
            product_list = products

        return product_list


class Wishlist(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'wishlist.html', {'products': products})


class About(View):
    def get(self, request):
        return render(request, 'about.html')
