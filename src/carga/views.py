from django.shortcuts import render
from django.views import generic

from .models import LastRefresh, Datasets

# Create your views here.

# view homepage
class Homepage(generic.ListView):
    model = Datasets
    template_name = "homepage.html"
    
    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)
        
        queryset = LastRefresh.objects.all().select_related('dataset_name', 'dataset_id')
        context["lastRefresh"] = queryset

        failedRefresh = LastRefresh.objects.filter(status = 'Failed').count()
        completeRefresh = LastRefresh.objects.filter(status = 'Completed').count()
        inProgressRefresh = LastRefresh.objects.filter(status = 'InProgress').count()

        context["failedRefresh"] = failedRefresh
        context["completeRefresh"] = completeRefresh
        context["inProgressRefresh"] = inProgressRefresh

        return context
