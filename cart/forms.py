from django import forms
from django.forms import ModelForm

# PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 26)]


class CartAddProductForm(forms.Form):
    # quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

# class CartAddProductForm(ModelForm):
#     class Meta:
#         widgets = {
#             'quantity': forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, attrs={'class': 'form-control'}),
#             'update': forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput, attrs={'class': 'form-control'}),
            
#         }
       

