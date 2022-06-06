from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify

from django.db.models import Q
from decimal import Decimal

from django.core.validators import MinValueValidator

from django.contrib.auth.models import User


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
    weight = models.IntegerField(default =0, null=True, blank=True)
    quantity = models.IntegerField("Quantité", default=0, blank=True, null=True)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE, verbose_name="Marque", blank=True, null=True)
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
        get_flavor = self.flavor if self.flavor is not None else ""
        get_brand = self.brand if self.brand is not None else ''
        get_ref = self.ref if self.ref is not None else ''
        slug = f"{get_brand}-{get_ref}-{get_name}-{get_flavor}-{get_weight}Kg-{self.id}"
        self.slug = slugify(slug)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        get_name = self.name.name if self.name is not None else ''
        get_brand = self.brand.name if self.brand is not None else ''
        get_weight = self.weight if self.weight != None else int(0)
        get_flavor = self.flavor if self.flavor is not None else ""
        get_ref = self.ref if self.ref is not None else ''
        if self.flavor is not None:
            return f"{get_name} {get_brand} {get_ref} {get_flavor} {get_weight}g"
        else:
            return f"{get_name} {get_brand} {get_ref} {get_weight}g"

    class Meta:
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
        db_table = 'Product'
        ordering = ['name__name', 'brand__name']


class Batch(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(unique=False, blank=True,null=True, max_length=255)
    ref = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField("Quantité", default=0, blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)
    expiring_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        get_product = self.product if self.product is not None else ''
        get_ref = self.ref if self.ref is not None else ''
        slug = f"{get_ref}-{get_product}"
        self.slug = slugify(slug)
        super(Batch, self).save(*args, **kwargs)

    def __str__(self):
        get_product = self.product if self.product is not None else ''
        get_ref = self.ref if self.ref is not None else ''
        return f"[{get_ref}] {get_product}"

    class Meta:
        verbose_name = 'Batch'
        verbose_name_plural = 'Batches'
        db_table = 'Batch'
        ordering = ['product','expiring_date']