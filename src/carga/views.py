from django.shortcuts import render
from django.views import generic

from .models import Datasets, RefreshHistory

# Create your views here.

# view homepage
class Homepage(generic.DetailView):
    model = RefreshHistory
    template_name = "homepage.html"
