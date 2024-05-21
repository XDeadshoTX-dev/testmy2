"""
Definition of urls for Lab3.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app.views import CustomLoginView
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         CustomLoginView.as_view
             (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year': datetime.now().year,
             }
         ),
         name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('searchProducts/', views.SearchProductsHTML.as_view(), name='searchProducts'),
    path('addProduct/', views.AddProductHTML.as_view(), name='addProduct'),
    path('deleteProduct/', views.DeleteProductHTML.as_view(), name='deleteProduct'),
    path('description/<int:product_id>', views.description_view, name='description'),
]
