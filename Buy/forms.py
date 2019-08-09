from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label="Nombre",)
    city = forms.CharField(label="Ciudad",)
    email = forms.EmailField(label="Correo Electrónico",)
    issue = forms.CharField(label="Asunto",)
    message = forms.CharField(label="Mensaje",
               widget=forms.Textarea,)