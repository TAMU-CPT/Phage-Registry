from django.db import models

class RegistryEntry(models.Model):
    owner = models.ForeignKey('auth.User')
    phagename = models.CharField(max_length=50, unique=True)
    exturl = models.CharField(max_length=1000, unique=True)
    verbose_name_plural = "Registry Entries"

    def __str__(self):
        return self.phagename
