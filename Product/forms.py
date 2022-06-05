from django import forms
from .models import (
    Brand,
    Color,
    Flavor,
    Product,
    Range
)
from Contact.models import Contact


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


class ColorForm(forms.ModelForm):
    name = forms.CharField(label="Nom de La Couleur",
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
        model = Color
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
        fields = ['name', 'weight','ref', 'brand', 'color', 'flavor', 'price', 'cost']
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
    price = forms.FloatField(label="Prix de Vente",
                                  required=False,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                          "step":"0.01",
                                      }
                                  ))
    cost = forms.FloatField(label="Prix d'Achat",
                                  required=False,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                          "step":"0.01",
                                      }
                                  ))
    ref = forms.CharField(label="Référence",
                                widget=forms.TextInput(
                                    attrs={
                                        "class": "form-control",
                                    }
                                ))
    brand = forms.ModelChoiceField(
        label="Marque",
        queryset=Brand.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    color = forms.ModelChoiceField(
        label="Couleur",
        queryset=Color.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data
