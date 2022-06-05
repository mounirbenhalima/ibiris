from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import datetime
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from .choices import STOCK_PROCESS

class OrderItem(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="user_loged",
                             blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(
        'Product.Product', on_delete=models.CASCADE, related_name='product_id')
    quantity = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    reminder = models.IntegerField(blank=True, null=True)
    identifier = models.CharField(max_length=255, null = True, blank=True)

    def __str__(self):
        return f'{self.quantity} de {self.item.product_designation}'

class Order(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             related_name="user_id",
                             blank=True, null=True)
    supplier = models.ForeignKey("Contact.Contact", related_name="Fournisseurs",
                                on_delete=models.SET_NULL, default=None, blank=True, null=True)
    company = models.ForeignKey("Company.Company", blank=True, null=True, on_delete = models.SET_NULL)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=False)
    items = models.ManyToManyField(OrderItem, blank=True, null=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    type_order = models.CharField(
        max_length=25, blank=True, null=True, choices=STOCK_PROCESS)

    category = models.CharField('Catégorie', max_length=255, null = True, blank= True)
    value = models.DecimalField(default =0, null=True, decimal_places=2 , max_digits=8 , blank=True)

    def __str__(self):
        return f'{self.ref_code}'

    def get_total(self):
        total = 0
        for item in self.items.all():
            total += item.quantity
        return total
    
    def get_amount(self):
        total = 0
        for item in self.items.all():
            total += item.quantity * item.price
        return total

    def get_absolute_url(self):
        return reverse("stock-manager:order-detail", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("stock-manager:order-delete", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        get_day = datetime.date.today().strftime("%m%d%y")
        if self.ref_code is None and self.id is not None:
            self.ref_code = get_slug = f'{get_day}-{self.user.id}{self.id}'
            self.slug = get_slug
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-ordered_date"]