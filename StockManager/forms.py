from django import forms
from django.db.models import Q
from .models import Order, OrderItem
from Contact.models import Contact
from Company.models import Company
from django.contrib.auth.models import User

class ContactChoiceForm(forms.ModelForm):

    supplier = forms.ModelChoiceField(
        required=False,
        queryset=Contact.objects.all(),
        label="Fournisseur",
        widget=forms.Select(
            attrs={
                "class": "form-control form-control-sm",
            }
        ))

    class Meta:
        model = Order
        fields = ["supplier"]