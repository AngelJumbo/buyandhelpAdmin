from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializar import DawSerializer
from django.shortcuts import get_object_or_404

# Create your views here.
def index1(request):
    return render(request, "index.html")


class DawList(generics.ListCreateAPIView):
    queryset = Articulo.objects.all()
    serializer_class = DawSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            pk = self.kwargs['pk'],
        )

        return obj
