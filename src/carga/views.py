from django.shortcuts import render
from django.views import generic

from .models import Datasets

# Create your views here.

# view homepage
class Homepage(generic.ListView):
    model = Datasets
    template_name = "homepage.html"
