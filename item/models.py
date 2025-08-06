from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    def __str__(self):
        return self.name
    
class Item(models.Model):
    category = models.ForeignKey(Category, related_name='item_category', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    description = models.TextField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    is_sold = models.BooleanField(default=False)
    item_image1 = models.ImageField(upload_to='item_images', blank=True, null=True)
    item_image2 = models.ImageField(upload_to='item_images', blank=True, null=True)
    item_image3 = models.ImageField(upload_to='item_images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name