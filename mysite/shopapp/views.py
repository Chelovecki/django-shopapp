"""
В этом модуле лежат различные наборы представлений.

 Содержатся разные view интернет-магазина: по товарам, заказам и т.д.
"""
from csv import DictWriter

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.core.cache import cache
from django.http import HttpResponseRedirect, JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView, CreateView, ListView, DetailView, DeleteView
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .common import save_csv_products
from .serializers import *


# from rest_framework.generics import GenericAPIView
# from rest_framework.mixins import ListModelMixin


class ProductDetailsView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'shopapp/product-details.html'


class ProductListView(ListView):
    # queryset-запрос
    queryset = Product.objects.filter(is_archived=False)
    # имя для обращения в html-документе
    context_object_name = 'products'
    # в каком html файле отрисовывать данные
    template_name = 'shopapp/products_list.html'


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'shopapp.add_product'

    model = Product
    fields = 'name', 'price', 'description', 'discount', 'created_by'

    # fields = 'name', 'price', 'description', 'discount'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('shopapp:products_list')


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    fields = 'name', 'price', 'description', 'discount'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:product_details',
            kwargs={'pk': self.object.pk},
        )

    def test_func(self):
        return ((self.get_object().created_by_id == self.request.user.pk)
                or
                (self.request.user.has_perms(['shopapp.change_product'])
                 ))


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.is_archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by('pk').all()
        products_data = [
            {
                'pk': product.pk,
                'name': product.name,
                'price': product.price,
                'is_archived': product.is_archived
            }
            for product in products
        ]

        return JsonResponse({'products': products_data})


@extend_schema(description="Product views CRUD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product
    Полный CRUD для сущностей товара
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,  # для поиска совпадений (аля regex)
        DjangoFilterBackend,  # фильтрация по search и по полному совпаднию
        OrderingFilter,
    ]

    search_fields = ["name", "description"]
    filterset_fields = [
        'name',
        'description',
        'price',
        'discount',
        'is_archived'
    ]
    ordering_fields = [
        'pk',
        'name',
        'description',
        'price',
        'discount',
        'is_archived'
    ]

    @extend_schema(
        summary="Get one product by ID",
        description='Retrieves product, returns 404 if not found',
        responses={
            200: ProductSerializer,  # а если ответ верный, то возвращается сериализатор (?)
            404: OpenApiResponse(description='Empty response, product by id not found'),
        }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @action(methods=["get"], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type="text/csv")

        filename = 'product-export.csv'
        response["Content-Disposition"] = f"attachment; filename={filename}"

        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            'name',
            'description',
            'price',
            'discount',
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })

        return response

    @action(methods=['post'], detail=False, parser_classes=[MultiPartParser])
    def upload_csv(self, request: HttpRequest):
        products = save_csv_products(
            request.FILES['file'].file,
            encoding=request.encoding
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class LatestProductsFeed(Feed):
    title = 'Shop products (latest)'
    description = 'New products are here'

    link = reverse_lazy('shopapp:products_list')

    def items(self):
        return (
            Product.objects.
            filter(is_archived=False).
            order_by('-created_at').
            all()
        )

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:50]


class OrdersListView(LoginRequiredMixin, ListView):
    permission_required = ['view_order']
    queryset = (
        Order.objects.select_related('user').prefetch_related('products')
    )


class OrdersDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'shopapp.view_order'
    template_name = 'shopapp/order_details.html'
    queryset = (
        Order.objects.select_related('user').prefetch_related('products')
    )


class OrdersCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'shopapp.add_order'

    template_name = 'shopapp/order_create.html'

    model = Order
    fields = ['user', 'delivery_address', 'promocode', 'products']

    def get_success_url(self):
        return reverse(
            'shopapp:order_details',
            kwargs={'pk': self.object.pk}
        )


class OrdersExportDataView(UserPassesTestMixin, View):
    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by('pk').all()
        orders_data = [
            {
                'ID': order.pk,
                'address': order.delivery_address,
                'promocode': order.promocode,
                'id_user': order.user.id,
                # 'products': [f'#{p.id}, `{p.name}`' for p in order.products.all()],
                'products': [
                    {'id': p.id, 'name': p.name}
                    for p in order.products.all()
                ],
            }
            for order in orders
        ]
        return JsonResponse({'orders': orders_data})

    def get_test_func(self):
        def test_func():
            return self.request.user.is_staff

        return test_func


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    filter_backends = [
        SearchFilter,  # для поиска совпадений (аля regex)
        DjangoFilterBackend,  # фильтрация по search и по полному совпаднию
        OrderingFilter
    ]

    search_fields = ["products", "delivery_address", 'user_id']
    filterset_fields = [
        'products',
        'delivery_address',
        'promocode',
        'created_at',
        'user_id'
    ]
    ordering_fields = [
        'pk',
        'user',
        'delivery_address'
    ]


class UserOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'shopapp/user_orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        self.owner: User = get_object_or_404(User, pk=user_id)

        return Order.objects.filter(user=user_id).select_related('user').prefetch_related('products')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_pk'] = self.owner.pk
        context['first_name'] = self.owner.profile.first_name
        context['last_name'] = self.owner.profile.last_name
        context['avatar'] = self.owner.profile.avatar.url if self.owner.profile.avatar else None

        return context


class ExportUserOrdersView(View):
    def get(self, *args, **kwargs) -> JsonResponse:
        user_pk = kwargs.get('pk')
        cache_name = f'user{user_pk}_orders_data_export'
        orders_data = cache.get(cache_name)
        if orders_data is None:
            user = get_object_or_404(User, id=user_pk)
            user_orders = (Order.objects.
                           filter(user=user_pk).
                           prefetch_related('products').
                           order_by('id').all()
                           )
            orders_data = [
                {
                    'ID': order.id,
                    'address': order.delivery_address,
                    'promocode': order.promocode,
                    'id_user': order.user.id,
                    # 'products': [f'#{p.id}, `{p.name}`' for p in order.products.all()],
                    'products': [
                        {'id': p.id, 'name': p.name}
                        for p in order.products.all()
                    ],
                }
                for order in user_orders
            ]
            cache.set(cache_name, orders_data, 150)

        return JsonResponse({'orders': orders_data})
