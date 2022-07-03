from django import forms

class MyForm(forms.Form):
    generic_input = forms.CharField()