from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from .models import Order, Product


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='abobus', password='b3g94568zslrfkudgh')

        add_order_permission = Permission.objects.get(codename='add_order')
        view_order_permission = Permission.objects.get(codename='view_order')
        add_product_permission = Permission.objects.get(codename='add_product')

        cls.user.user_permissions.add(add_order_permission)
        cls.user.user_permissions.add(view_order_permission)
        cls.user.user_permissions.add(add_product_permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        self.client.force_login(user=self.user)

        self.product = Product.objects.create(
            name='Pencil',
            price='199.00',
            description='lil penCil',
            created_by=self.user,
        )

        self.order = Order.objects.create(
            user=self.user,
            delivery_address='куда-то',
            promocode='25634',
        )

        self.order.products.add(self.product)

    def tearDown(self):
        self.order.delete()
        self.product.delete()

    def test_order_details(self):
        url_to_details = reverse('shopapp:order_details', kwargs={'pk': self.order.pk})
        response = self.client.get(url_to_details)

        self.assertEqual(response.status_code, 200)
        # print(response.context)
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertEqual(response.context['order'].pk, self.order.pk)


class OrdersExportDataViewTestCase(TestCase):
    fixtures = [
        'users-fixtures.json',
        'products-fixtures.json',
        'orders-fixtures.json',
    ]
    def test_get_order_view(self):
        response = self.client.get(reverse('shopapp:order_export'))
        print(response)

        self.assertRedirects(response, str(settings.LOGIN_REDIRECT_URL))
        self.assertEqual(response.status_code, 200)
    def test_staff_user(self):
        self.client.force_login()
