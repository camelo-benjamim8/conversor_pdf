from django.db import models

# Create your models here.
class FileDelete(models.Model):
    filename = models.CharField(max_length=250)
    data_deletar = models.CharField(max_length=250)
    def __str__(self):
        return self.filename