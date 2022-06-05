from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify

from django.db.models import Q
from decimal import Decimal

from django.core.validators import MinValueValidator

from django.contrib.auth.models import User
from StockManager.models import Order


class Brand(models.Model):
    name = models.CharField(
        "Marque",
        max_length=200,
        unique=True
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product:brand-update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("product:brand-delete", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Marque'
        verbose_name_plural = 'Marques'
        db_table = 'Brand'
        ordering = ['id']

class Color(models.Model):
    name = models.CharField(
        "Couleur",
        max_length=200,
        unique=True,
    )

    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse("product:color-update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("product:color-delete", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.slug = slugify(self.name)
        super(Color, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Couleur'
        verbose_name_plural = 'Couleurs'
        db_table = 'Color'
        ordering = ["id"]

class Flavor(models.Model):
    name = models.CharField(
        "Parfum",
        max_length=200,
        unique=True,
    )

    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse("product:flavor-update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("product:flavor-delete", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Flavor, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Parfum'
        verbose_name_plural = 'Parfums'
        ordering = ["name"]

class Range(models.Model):
    slug = models.SlugField(unique=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    

    def get_absolute_url(self):
        return reverse("product:range-update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("product:range-delete", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.slug = slugify(self.name)

        super(Range, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Gamme'
        verbose_name_plural = 'Gammes'
        db_table = 'Range'
        ordering = ['id']


class Product(models.Model):
    name = models.ForeignKey(
        'Range', on_delete=models.SET_NULL, blank=True, null=True)
    slug = models.SlugField(unique=False, blank=True,
                            null=True, max_length=255)
    ref = models.CharField(max_length=200, null=True, blank=True)
    product_designation = models.CharField(max_length=200, null=True, blank=True)
    weight = models.DecimalField(default =0, null=True,decimal_places=1, max_digits=5, blank=True)
    quantity = models.IntegerField("Quantité", default=0, blank=True, null=True)
    threshold = models.PositiveIntegerField("Seuil", default=0, blank=True, null=True)
    price = models.FloatField('Prix',default = 0, null=True, blank=True)
    cost = models.FloatField('Coût',default = 0, null=True, blank=True)
    flavor = models.ForeignKey('Flavor', on_delete=models.SET_NULL, blank=True, null= True)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE, verbose_name="Marque", blank=True, null=True)
    color = models.ForeignKey("Color", on_delete=models.CASCADE, verbose_name="Couleur", blank=True, null=True)
    flavor = models.ForeignKey("Flavor", on_delete=models.CASCADE, verbose_name="Parfum", blank=True, null=True)

    def get_delete_url(self):
        return reverse("product:product-delete", kwargs={"slug": self.slug})

    def get_add_to_order_url(self):
        return reverse("stock-manager:add-to-order", kwargs={"slug": self.slug})

    def get_absolute_url(self):
        return reverse("product:product-update", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        get_name = self.name.name if self.name is not None else ''
        get_weight = self.weight if self.weight != None else int(0)
        get_color = self.color if self.color != None and self.color.name != 'autre' else ""
        get_flavor = self.flavor if self.flavor is not None else ""
        get_brand = self.brand if self.brand is not None else ''
        get_ref = self.ref if self.ref is not None else ''
        slug = f"{get_brand}-{get_ref}-{get_name}-{get_flavor}-{get_color}-{get_weight}Kg-{self.id}"
        if self.slug is None:
            self.slug = slugify(slug)
        self.product_designation = ' '.join(self.__str__().split()).upper()
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        get_name = self.name.name if self.name is not None else ''
        get_weight = self.weight if self.weight != None else int(0)
        get_color = self.color if self.color != None and self.color.name != 'autre' else ""
        get_flavor = self.flavor if self.flavor is not None else ""
        get_ref = self.ref if self.ref is not None else ''
        if self.flavor is not None:
            return f"[{self.brand.name} {get_ref}] {get_name} {get_flavor} {get_color} {get_weight} g"
        else:
            return f"[{self.brand.name} {get_ref}] {get_name} {get_color} {get_weight} g"

    
    def bought_quantity(self, start_date, end_date):
        orders = Order.objects.filter(Q(ordered_date__lte = end_date) & Q(ordered_date__gte = start_date) & Q(type_order = "STOCK_ENTRY"))
        total = 0
        for o in orders:
            for i in o.items.all():
                if i.item == self:
                    total += i.quantity
        
        return total
    
    def sold_quantity(self, start_date, end_date):
        orders = Order.objects.filter(Q(ordered_date__lte = end_date) & Q(ordered_date__gte = start_date) & Q(type_order = "STOCK_OUT"))
        total = 0
        for o in orders:
            for i in o.items.all():
                if i.item == self:
                    total += i.quantity
        
        return total

    def product_cost(self, start_date, end_date):
        orders = Order.objects.filter(Q(ordered_date__lte = end_date) & Q(ordered_date__gte = start_date) & Q(type_order = "STOCK_ENTRY"))
        total = 0
        for o in orders:
            for i in o.items.all():
                if i.item == self:
                    total += i.quantity * i.price
        
        return total
    
    def benefit(self, start_date, end_date):
        orders = Order.objects.filter(Q(ordered_date__lte = end_date) & Q(ordered_date__gte = start_date) & Q(type_order = "STOCK_OUT"))
        total = 0
        for o in orders:
            for i in o.items.all():
                if i.item == self:
                    total += i.quantity * i.price
        
        return total
    class Meta:
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
        db_table = 'Product'
        ordering = ['name__name', 'brand__name']