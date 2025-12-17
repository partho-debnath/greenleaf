from django.shortcuts import render
from django.core.paginator import Paginator
from django.views import generic

from .models import Product


class ProductListView(generic.ListView):
    template_name = "tree_list.html"
    queryset = Product.objects.select_related(
        "category"
    ).order_by("id").all()
    paginator_class = Paginator
    paginate_by = 2

    def get_queryset(self):
        return super().get_queryset()


class ProductDetailsView(generic.DetailView):
    template_name = "tree_list.html"
    queryset = Product.objects.defer("thumbnail").select_related(
        "category"
    ).order_by("id").all()
