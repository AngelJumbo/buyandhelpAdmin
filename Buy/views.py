from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializar import ArticuloSerializer
from django.shortcuts import get_object_or_404

# Create your views here.
def index1(request):
    return render(request, "index.html")


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

class ArticulosDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer
