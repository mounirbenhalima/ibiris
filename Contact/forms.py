from django import forms
from . models import Contact


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(label="Prénom",
                                 required=False,
                                 widget=forms.TextInput(
                                     attrs={
                                         "class": "form-control",
                                         "type": "text",
                                     }
                                 ))
    last_name = forms.CharField(label="Nom",
                                 required=False,
                                 widget=forms.TextInput(
                                     attrs={
                                         "class": "form-control",
                                         "type": "text",
                                     }
                                 ))
    company = forms.CharField(label="Entreprise",
                                 required=True,
                                 widget=forms.TextInput(
                                     attrs={
                                         "class": "form-control",
                                         "type": "text",
                                     }
                                 ))
    email = forms.EmailField(label="Email",
        required=False,
        widget=forms.TextInput(
         attrs={
             "class": "form-control",
             "type": "email",
         }
     ))
    

    phone_number = forms.CharField(label="Téléphone",
                                 required=False,
                                 widget=forms.TextInput(
                                     attrs={
                                         "class": "form-control",
                                         "type": "text",
                                     }
                                 ))
    address = forms.CharField(label="Adresse",
                                 required=False,
                                 widget=forms.TextInput(
                                     attrs={
                                         "class": "form-control",
                                         "type": "text",
                                     }
                                 ))

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name','company', 'email', "phone_number", "address"]