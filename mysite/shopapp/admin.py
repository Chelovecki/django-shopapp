from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Product, Order


@admin.action(description='Archive them')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(is_archived=True)
    mark_archived.short_description = "Mark selected products as archived"


@admin.action(description='Unarchive them')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(is_archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name', 'created_by', 'description_short', 'price', 'discount', 'is_archived',
    list_display_links = 'pk', 'name'
    ordering = 'pk',
    search_fields = 'name', 'description'

    fieldsets = [
        ('Main', {
            'fields': ('name', 'description')
        }),

        ('Price options', {
            'fields': ('price', 'discount'),
            'classes': ('collapse', ' wide'),
        }),

        ('Extra options', {
            'fields': ('is_archived', 'created_by'),
            'classes': ('collapse', ' wide'),
            'description': 'Extra Options. Use for soft-delete',
        }),
    ]
    actions = [
        mark_archived,
        mark_unarchived,
        'export'
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) > 48:
            return obj.description[:48] + "..."
        else:
            return obj.description


class ProductInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'delivery_address', 'promocode', 'created_at', 'username'

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, obj: Order):
        return obj.user.first_name or obj.user.username

    def username(self, obj: Product) -> str:
        return obj.user.first_name or obj.user.username

    username.short_description = 'User'

