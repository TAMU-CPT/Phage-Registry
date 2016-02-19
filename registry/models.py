from django.db import models
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _


class DatabaseSource(models.Model):
    name = models.CharField(max_length=50)
    template_url = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class RegistryEntry(models.Model):
    owner = models.ForeignKey('auth.User')
    phagename = models.CharField(max_length=50, unique=True)
    extid = models.CharField(max_length=1000, unique=True)
    verbose_name_plural = "Registry Entries"
    alias_list = models.CharField(max_length=2000, null=True, blank=True)
    database = models.ForeignKey(DatabaseSource, null=True, blank=True)


    def __str__(self):
        return self.phagename

    def clean(self):
        super(RegistryEntry, self).clean()

        self.phagename = str(self.phagename)
        print self.phagename[0]

        if len(self.phagename) < 4:
            raise ValidationError("Phage name is too short")

        if self.phagename[0] != self.phagename[0].upper():
            raise ValidationError("Must start with capital letter")

        if len(self.phagename) > 14:
            raise ValidationError("Phage name is too long")

        if not self.phagename.isalnum():
            raise ValidationError("Phage name may only use alphanumeric characters")

        return True


class RegistryEntryForm(ModelForm):
    class Meta:
        model = RegistryEntry
        fields = ('phagename', 'extid', 'alias_list', 'database')
        labels = {
            'phagename': _('Phage Name'),
            'extid': _('External ID'),
            'alias_list': _('Aliases'),
        }

        help_texts = {
            'extid': _('External ID appropriate to the database. For NCBI references this is one of the ID numbers, for PBI phages this is the phage name'),
            'alias_list': _('Sometimes phages have "official" names which are complex and hard to remember (e.g. vB_CcrM-Colossus). You can specify those here as a comma separated list.'),
        }

