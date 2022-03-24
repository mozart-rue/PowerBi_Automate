from django.shortcuts import render
from django.views import generic

from .models import Datasets, RefreshHistory

# Create your views here.

# view homepage
class Homepage(generic.ListView):
    model = RefreshHistory
    template_name = "homepage.html"
    
    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)
        # Filtrar a tabela de filmes pegando os filmes com categoria é igual a categoria do filme da pagina
        historicoDetalhado = RefreshHistory.objects.distinct('dataset_name')
        context["historicoDetalhado"] = historicoDetalhado

        failedRefresh = RefreshHistory.objects.filter(status = 'Failed').count()
        completeRefresh = RefreshHistory.objects.filter(status = 'Completed').count()
        context["failedRefresh"] = failedRefresh
        context["completeRefresh"] = completeRefresh

        return context
