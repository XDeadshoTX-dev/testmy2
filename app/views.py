from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
import re

from app.models import Product

"""
Definition of views.
"""

from datetime import datetime
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from app.forms import RegisterForm
from django.shortcuts import render, redirect
from django.http import HttpRequest


class ProductsManager:
    def DeleteProducts():
        Product.objects.all().delete()

    def GetProducts():
        products = Product.objects.all()
        for product in products:
            product.product_stars_range = range(product.Product_stars)
        return products

    def SearchProducts(name):
        if name:
            products = Product.objects.filter(
                Product_name__regex=r'^.*{}.*$'.format(re.escape(name)))
            return products
        else:
            # Return empty queryset if name is not provided
            return Product.objects.none()

    def DeleteProduct(name):
        if name:
            Product.objects.filter(Product_name=name).delete()
        else:
            # Return error message if name is not provided
            return JsonResponse({"status": "error",
                                 "message": "Product name must be provided"})

    def AddProduct(name, description, image_url, image, stars,
                   available_quantity, old_price, single_price):
        # Perform validation checks on required fields
        if name and description and stars and available_quantity and single_price:
            # Convert stars, available_quantity, and single_price to the correct data types
            try:
                stars = int(stars)
                available_quantity = int(available_quantity)
                single_price = float(single_price)
            except (ValueError, TypeError):
                # Return error response if conversion fails
                return JsonResponse(
                    {"status": "error", "message": "Invalid input data types"})

            # Check if stars and available_quantity are non-negative
            if stars < 0 or available_quantity < 0:
                return JsonResponse({"status": "error",
                                     "message": "Stars and available quantity must be non-negative"})

            # Check if single_price is positive
            if single_price <= 0:
                return JsonResponse({"status": "error",
                                     "message": "Single price must be positive"})

            # Add the product
            new_product = Product(
                Product_name=name,
                Product_description=description,
                Product_image_url=image_url,  # link image
                Product_image=image,
                # file from directory app/Product_images/{file}.{format}
                Product_stars=stars,
                Product_available_quantity=available_quantity,
                Product_old_price=old_price,
                Product_single_price=single_price
            )
            new_product.save()
            # Return success response
            return JsonResponse(
                {"status": "success", "message": "Product added successfully"})
        else:
            # Return error response if any required field is missing
            return JsonResponse({"status": "error",
                                 "message": "All required fields must be provided"})


class SearchProductsHTML(View):
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            name = request.GET.get("search_request", None)
            if name:
                products = ProductsManager.SearchProducts(name)
                return render(
                    request,
                    'app/index.html',
                    {
                        'title': 'Result search',
                        'year': datetime.now().year,
                        'available_products': products,
                    }
                )


class DeleteProductHTML(View):
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            name = request.GET.get('product_name', None)
            if name:
                # Delete the product
                ProductsManager.DeleteProduct(name)
                # Return success response
                return JsonResponse({"status": "success",
                                     "message": "Product deleted successfully"})
            else:
                # Return error response if product name is missing
                return JsonResponse(
                    {"status": "error", "message": "Product name is required"})


class AddProductHTML(View):
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            name = request.GET.get('product_name', None)
            description = request.GET.get('product_description', None)
            image_url = request.GET.get('product_image_url', None)
            image = request.GET.get('product_image',
                                    None)  # Directory must be in app/Product_images/file.jpg
            stars = request.GET.get('product_stars', None)
            available_quantity = request.GET.get('product_available_quantity',
                                                 None)
            old_price = request.GET.get('product_old_price', None)
            single_price = request.GET.get('product_single_price', None)

            ProductsManager.AddProduct(name, description, image_url, image,
                                       stars, available_quantity, old_price,
                                       single_price)


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    # ProductsManager.DeleteProducts()
    # ProductsManager.AddProduct("Pineapple", "Pineapple description", None, "app/Product_images/Pineapple.jpg", 4, 142, 15.99, 9.99)
    # ProductsManager.AddProduct("Cactus", "Cactus description", "https://st.depositphotos.com/1004370/2187/i/450/depositphotos_21876019-stock-illustration-cactus.jpg", None, 2, 0, None, 20.3)
    # ProductsManager.AddProduct("Apple Pro Plus Ultra Max 1024gb", "Apple description", "https://static.wikia.nocookie.net/minecraft/images/0/0c/GoldenApple.gif/revision/latest/scale-to-width/360?cb=20190916004559", None, 5, 64, None, 199.99)
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
            'available_products': ProductsManager.GetProducts(),
        }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Contact',
            'message': 'Your contact page.',
            'year': datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'About',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        }
    )


def description_view(request, product_id):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    product = Product.objects.get(Product_id=product_id)
    return render(
        request,
        'app/description.html',
        {
            'title': 'Description product',
            'year': datetime.now().year,
            'product': product,
        }
    )


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'app/register.html',
                  {'form': form, 'title': 'Register',
                   'year': datetime.now().year})


class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


def custom_logout_view(request):
    logout(request)
    return redirect('home')
