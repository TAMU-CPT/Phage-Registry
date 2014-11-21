from django.db import models
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form, CharField, PasswordInput
from django.utils.translation import ugettext_lazy as _


class RegistryEntry(models.Model):
    owner = models.ForeignKey('auth.User')
    phagename = models.CharField(max_length=50, unique=True)
    exturl = models.CharField(max_length=1000, unique=True)
    verbose_name_plural = "Registry Entries"
    alias_list = models.CharField(max_length=2000, null=True, blank=True)

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
        fields = ('phagename', 'exturl', 'alias_list')
        labels = {
            'phagename': _('Phage Name'),
            'exturl': _('External URL'),
            'alias_list': _('Aliases'),
        }

        help_texts = {
            'exturl': _('Much like how a DOI points permanently at a document, this URL should be a permanent record of that phage that people can access in years to come. This may be a GenBank/RefSeq record, or it may be another public database.'),
            'alias_list': _('Sometimes phages have "official" names which are complex and hard to remember (e.g. vB_CcrM-Colossus). You can specify those here as a comma separated list.'),
        }

