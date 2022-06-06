from django import forms
from .models import (
    Brand,
    Flavor,
    Product,
    Range
)


class BrandForm(forms.ModelForm):
    name = forms.CharField(
        label="Nom de La Marque",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
            }
        ))

    def clean(self):
        cleaned_data = super().clean()
        self.cleaned_data['name'] = cleaned_data['name'].lower()
        return self.cleaned_data

    class Meta:
        model = Brand
        exclude = ('slug',)
        fields = "__all__"

class RangeForm(forms.ModelForm):
    name = forms.CharField(
        label="Nom de La Gamme",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
            }
        ))

    def clean(self):
        cleaned_data = super().clean()
        self.cleaned_data['name'] = cleaned_data['name'].lower()
        return self.cleaned_data

    class Meta:
        model = Range
        exclude = ('slug',)
        fields = "__all__"


class FlavorForm(forms.ModelForm):
    name = forms.CharField(label="Parfum",
                           required=True,
                           widget=forms.TextInput(
                               attrs={
                                   "class": "form-control",
                                   "type": "text",
                               }
                           ))

    def clean(self):
        cleaned_data = super().clean()
        self.cleaned_data['name'] = cleaned_data['name'].lower()
        return self.cleaned_data

    class Meta:
        model = Flavor
        exclude = ('slug',)
        fields = "__all__"

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'weight','ref', 'brand', 'flavor']
    name = forms.ModelChoiceField(
        label="Gamme",
        queryset=Range.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    flavor = forms.ModelChoiceField(
        label="Parfum",
        required=False,
        queryset=Flavor.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    weight = forms.IntegerField(label="Poids Unitaire",
                                  required=False,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                      }
                                  ))
    ref = forms.CharField(label="Référence",
                                required=False,
                                widget=forms.TextInput(
                                    attrs={
                                        "class": "form-control",
                                    }
                                ))
    brand = forms.ModelChoiceField(
        label="Marque",
        required=False,
        queryset=Brand.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data
