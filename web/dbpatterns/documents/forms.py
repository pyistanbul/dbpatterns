from django import forms

__author__ = 'fatiherikli'

class DocumentForm(forms.Form):
    title = forms.CharField("Document title")