from django.db import models

# Create your models here.

# Datasets Model
class Datasets(models.Model):
    dataset_id = models.TextField(primary_key=True, max_length=255)
    name = models.TextField(blank=True, null=True)
    dataset_url = models.TextField(db_column='dataset_url', blank=True, null=True)  # Field name made lowercase.
    isrefreshable = models.BooleanField(db_column='isRefreshable', blank=True, null=True)  # Field name made lowercase.
    isonpremgatewayrequired = models.BooleanField(db_column='isOnPremGatewayRequired', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'datasets'

    def __str__(self):
        return self.name


# Datasources Model
class Datasources(models.Model):
    dataset_id = models.CharField(primary_key=True, max_length=255)
    dataset_name = models.CharField(max_length=50)
    datasource_name = models.CharField(max_length=50, blank=True, null=True)
    datasource_id = models.CharField(max_length=255)
    gateway_id = models.CharField(max_length=255)
    gateway_name = models.CharField(max_length=50, blank=True, null=True)
    gateway_status = models.CharField(max_length=25, blank=True, null=True)
    conection_type = models.CharField(max_length=25, blank=True, null=True)
    cred_type = models.CharField(max_length=25, blank=True, null=True)
    inserted_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'datasources'

    def __str__(self):
        return self.datasource_name


# Gateways Model
class Gateways(models.Model):
    dataset_name = models.CharField(max_length=50)
    datasource_name = models.CharField(max_length=50, blank=True, null=True)
    datasource_id = models.CharField(max_length=255)
    gateway_id = models.CharField(max_length=255)
    gateway_name = models.CharField(max_length=50, blank=True, null=True)
    datasource_status = models.CharField(max_length=12)
    inserted_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'gateways'

    def __str__(self):
        return self.gateway_name


# RefreshHistory Model
class RefreshHistory(models.Model):
    dataset_name = models.CharField(max_length=50)
    dataset_id = models.CharField(max_length=255)
    status = models.CharField(max_length=25, blank=True, null=True)
    refresh_type = models.CharField(max_length=25)
    request_id = models.CharField(primary_key=True,max_length=255)
    history_id = models.CharField(max_length=255)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    total_time = models.TimeField()
    inserted_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'refresh_history'

    def __str__(self):
        return self.dataset_name


# ScheduleRefresh Model
class ScheduledRefresh(models.Model):
    dataset_name = models.CharField(max_length=50)
    dataset_id = models.CharField(max_length=255)
    ativo = models.BooleanField()
    atualizacao = models.TimeField(blank=True, null=True)
    inserted_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'scheduled_refresh'

    def __str__(self):
        return self.dataset_name_name