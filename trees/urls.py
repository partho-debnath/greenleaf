from django.urls import path

from .views import (
    ProductListView, ProductDetailsView,
)

app_name = "trees"
urlpatterns = [
    path(route="", view=ProductListView.as_view(), name="tree_list"),
    path(
        route="<slug:slug>/tree-details/",
        view=ProductDetailsView.as_view(),
        name="tree_details",
    ),
]
