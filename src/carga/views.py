from django.shortcuts import render
from django.views import generic

from .models import LastRefresh, RefreshHistory

# Create your views here.

# view homepage
class Homepage(generic.ListView):
    model = LastRefresh
    template_name = "homepage.html"
    
    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)
        # Filtrar a tabela de filmes pegando os filmes com categoria é igual a categoria do filme da pagina
        last_refresh = LastRefresh.objects.distinct('dataset_name')
        context["lastRefresh"] = last_refresh

        failedRefresh = LastRefresh.objects.filter(status = 'Failed').count()
        completeRefresh = LastRefresh.objects.filter(status = 'Completed').count()
        inProgressRefresh = LastRefresh.objects.filter(status = 'InProgress').count()

        context["failedRefresh"] = failedRefresh
        context["completeRefresh"] = completeRefresh
        context["inProgressRefresh"] = inProgressRefresh

        return context
