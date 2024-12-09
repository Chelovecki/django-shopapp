from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

app_name = 'shopapp'

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)

urlpatterns = [
    # path("", ShopIndexView.as_view(), name="index"),
    path("api/", include(routers.urls)),
    # path("groups/", GroupsListView.as_view(), name="groups_list"),

    path("products/",   ProductListView.as_view(), name="products_list"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/export/", ProductsDataExportView.as_view(), name="products_export"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name="product_archive"),

    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/create/", OrdersCreateView.as_view(), name="order_create"),
    path("orders/export/", OrdersExportDataView.as_view(), name="order_export"),
    path("orders/<int:pk>/", OrdersDetailView.as_view(), name="order_details"),
]
