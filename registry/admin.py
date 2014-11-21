from django.contrib import admin
from .models import RegistryEntry, DatabaseSource

# Register your models here.
admin.site.register(RegistryEntry)
admin.site.register(DatabaseSource)
