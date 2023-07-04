from django.db import models


# Create your models here.
class CO2(models.Model):
    date = models.DateField()
    average = models.FloatField()

    class Meta:
        ordering = ('date',)


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


# class InvoicesOut(CAPDbBase):
#     date = CAPDbBase.objects.get_queryset()
