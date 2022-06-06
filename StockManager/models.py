from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import datetime
from django.utils.text import slugify
from django.shortcuts import get_object_or_404

class Purchase(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             related_name="purchase_user",
                             blank=True, null=True)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=False)
    order_date = models.DateTimeField(blank=True, null=True)
    batch = models.ForeignKey('Product.Batch', on_delete=models.CASCADE, related_name='purchase_product')
    quantity = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.ref_code}'

    def save(self, *args, **kwargs):
        get_ref = self.ref_code if self.ref_code is not None else ""            
        self.slug = slugify(get_ref)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-order_date"]

class Consumption(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             related_name="consumption_user",
                             blank=True, null=True)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=False)
    order_date = models.DateTimeField(blank=True, null=True)
    batch = models.ForeignKey('Product.Batch', on_delete=models.CASCADE, related_name='consumption_product')
    quantity = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.ref_code}'

    def save(self, *args, **kwargs):
        get_ref = self.ref_code if self.ref_code is not None else ""            
        self.slug = slugify(get_ref)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-order_date"]