from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.db.models import Q

class Contact(models.Model):
    slug = models.SlugField(max_length=255)
    company = models.CharField(
        "Entreprise", max_length=200, null=True, blank=True)
    last_name = models.CharField(
        "Nom de Famille", max_length=200, null=True, blank=True)
    first_name = models.CharField(
        "Prénom", max_length=200, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(
        'Numero de Téléphone', max_length=10, blank=True, null=True)
    address = models.CharField(
        "Adresse", max_length=255, blank=True, null=True)

    region = models.CharField(
        "Wilaya", max_length=255, blank=True, null=True
    )
    def get_absolute_url(self):
        return reverse("contact:update-contact", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("contact:delete-contact", kwargs={"slug": self.slug})

    def __str__(self):
        return f'{self.company} {self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):

        self.slug = slugify(f'{self.id} {self.first_name} {self.last_name}')

        super(Contact, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
        db_table = 'Supplier'
        ordering = ['first_name']
