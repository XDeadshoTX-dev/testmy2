"""
Definition of models.
"""

from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Product(models.Model):
    Product_id = models.AutoField(primary_key=True)  # Product ID (AutoField)
    Product_name = models.CharField(max_length=100, default="Unknown product")  # Product name (String)
    Product_description = models.TextField(default="Unknown description")  # Product description (String)
    Product_image_url = models.URLField(null=True, blank=True, default=None)  # Product URL image (url)
    Product_image = models.ImageField(upload_to='app\\static\\app\\Product_images\\', null=True, blank=True, default=None)  # Product image (file)
    Product_stars = models.IntegerField(default=0)  # Product stars (Integer)
    Product_available_quantity = models.IntegerField(default=0)  # Product available quantity (Integer)
    Product_old_price = models.FloatField(default=0.0, null=True)  # Product old price (Float)
    Product_single_price = models.FloatField(default=0.0)  # Product single price (Float)

    def __str__(self):
        return self.Product_name

    def clean(self):
        if not self.Product_image_url and not self.Product_image:
            raise ValidationError('Either Product_image_url or Product_image must be provided.')
        if self.Product_image_url and self.Product_image:
            raise ValidationError('Only one of Product_image_url or Product_image should be provided.')

    def save(self, *args, **kwargs):
        self.clean()
        super(Product, self).save(*args, **kwargs)