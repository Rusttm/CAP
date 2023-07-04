from django.contrib import admin

# Register your models here.
from .models import CO2, InvoicesOut

admin.site.register(CO2)
admin.site.register(InvoicesOut)
