from django.db import models


# Create your models here.
class CO2(models.Model):
    date = models.DateField()
    average = models.FloatField()

    class Meta:
        ordering = ('date',)


# from https://stackoverflow.com/questions/3519143/django-how-to-specify-a-database-for-a-model
class CAPDbManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()

        # if `use_db` is set on model use that for choosing the DB
        if hasattr(self.model, 'use_db'):
            qs = qs.using(self.model.use_db)

        return qs


class CAPDbBase(models.Model):
    use_db = 'cap_db'
    objects = CAPDbManager()

    class Meta:
        abstract = True


class InvoicesOut(models.Model):
    moment = models.DateField()
    sum = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'invoices_out_table'
