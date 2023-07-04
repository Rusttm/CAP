from django.db import models


# Create your models here.
class CO2(models.Model):
    date = models.DateField()
    average = models.FloatField()

    class Meta:
        ordering = ('date',)


# from https://stackoverflow.com/questions/3519143/django-how-to-specify-a-database-for-a-model

class InvoicesOut(models.Model):
    moment = models.DateField()
    sum = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'invoices_out_table'
