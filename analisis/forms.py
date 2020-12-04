from django import forms

class Guardar(forms.Form):
    nombre = forms.CharField(label="Nombre del archivo", max_length=100)