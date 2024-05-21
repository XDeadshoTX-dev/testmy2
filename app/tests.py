"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import django
from django.test import TestCase, Client
from django.urls import reverse
from app.models import Product
from app.views import ProductsManager

# TODO: Configure your database in settings.py and sync before running tests.

class ViewTest(TestCase):
    """Tests for the application views."""

    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            super(ViewTest, cls).setUpClass()
            django.setup()

    # def test_home(self):
    #     """Tests the home page."""
    #     response = self.client.get('/')
    #     self.assertContains(response, 'Home Page', 1, 200)

    # def test_contact(self):
    #     """Tests the contact page."""
    #     response = self.client.get('/contact/')
    #     self.assertContains(response, 'Contact', 3, 200)

    # def test_about(self):
    #     """Tests the about page."""
    #     response = self.client.get('/about/')
    #     self.assertContains(response, 'About', 3, 200)
        
class ProductsManagerTestCase(TestCase):
    def setUp(self):
        self.product1 = Product.objects.create(Product_name="Test Product 1", Product_description="Description 1", Product_image_url = "https://target.scene7.com/is/image/Target/GUEST_cf4773e6-afec-4aa1-89e7-74b7dfc09973?wid=488&hei=488&fmt=pjpeg", Product_stars=4, Product_available_quantity=10, Product_single_price=19.99)
        self.product2 = Product.objects.create(Product_name="Test Product 2", Product_description="Description 2", Product_image_url = "https://target.scene7.com/is/image/Target/GUEST_cf4773e6-afec-4aa1-89e7-74b7dfc09973?wid=488&hei=488&fmt=pjpeg", Product_stars=3, Product_available_quantity=5, Product_single_price=29.99)
        self.product3 = Product.objects.create(Product_name="Test Product 3", Product_description="Description 3", Product_image_url = "https://target.scene7.com/is/image/Target/GUEST_cf4773e6-afec-4aa1-89e7-74b7dfc09973?wid=488&hei=488&fmt=pjpeg", Product_stars=5, Product_available_quantity=20, Product_single_price=9.99)
        self.client = Client()

    def test_get_products(self):
        products = ProductsManager.GetProducts()
        self.assertEqual(len(products), 3)

    def test_search_products(self):
        products = ProductsManager.SearchProducts("Test Product 1")
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].Product_name, "Test Product 1")

        products = ProductsManager.SearchProducts("Test")
        self.assertEqual(len(products), 3)

        products = ProductsManager.SearchProducts("Non-existent Product")
        self.assertEqual(len(products), 0)

    def test_delete_product(self):
        ProductsManager.DeleteProduct("Test Product 1")
        products = ProductsManager.GetProducts()
        self.assertEqual(len(products), 2)

        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(Product_name="Test Product 1")

    # def test_add_product(self):
    #     response = ProductsManager.AddProduct("New Product", "New Description", "", None, 4, 15, None, 24.99)
    #     self.assertEqual(response.status_code, 200)

    #     products = ProductsManager.GetProducts()
    #     self.assertEqual(len(products), 4)
    #     self.assertEqual(products[3].Product_name, "New Product")
        
    # def test_search_products_view(self):
    #     response = self.client.get(reverse('searchProducts'), {'search_request': 'Test'})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'app/index.html')
    #     self.assertIn('available_products', response.context)
    #     self.assertEqual(len(response.context['available_products']), 3)
