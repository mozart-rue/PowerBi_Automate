from django.contrib import admin
from .models import Datasets, Datasources, Gateways, RefreshHistory, ScheduledRefresh

# Register your models here.
admin.site.register(Datasets)
admin.site.register(Datasources)
admin.site.register(Gateways)
admin.site.register(RefreshHistory)
admin.site.register(ScheduledRefresh)
