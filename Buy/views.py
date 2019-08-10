from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializar import ArticuloSerializer
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from .forms import ContactForm
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


# Create your views here.
#index
def index1(request):
    return render(request, "index.html")

#formulario contactenos
class ContactView(TemplateView):
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_form'] = ContactForm()

        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        city = request.POST.get('city')
        email = request.POST.get('email')
        issue = request.POST.get('issue')
        message = request.POST.get('message')

        body = render_to_string(
            'email_content.html', {
                'name': name,
                'city': city,
                'email': email,
                'issue': issue,
                'message': message,
            },
        )

        email_message = EmailMessage(
            subject='Mensaje de usuario',
            body=body,
            from_email='milton.garcia1998@hotmail.com',
            to=['milton.garcia1998@hotmail.com'],
        )
        email_message.content_subtype = 'html'
        email_message.send()


        return redirect('contact')

#API REST
#get, post
class ArticulosList(generics.ListCreateAPIView):
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            pk = self.kwargs['pk'],
        )

        return obj

#updtate, delete
class ArticulosDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer
