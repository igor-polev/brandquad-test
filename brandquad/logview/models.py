from django.db import models

# Ngnix log table
class NgnixLog(models.Model):
    time        = models.DateTimeField()
    remote_ip   = models.CharField(max_length=15)
    remote_user = models.CharField(max_length=64)
    method      = models.CharField(max_length=8)
    request_uri = models.CharField(max_length=2048)
    response    = models.IntegerField()
    bytes       = models.IntegerField()