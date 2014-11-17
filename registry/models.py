from django.db import models
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form, CharField, PasswordInput

class RegistryEntry(models.Model):
    owner = models.ForeignKey('auth.User')
    phagename = models.CharField(max_length=50, unique=True)
    exturl = models.CharField(max_length=1000, unique=True)
    verbose_name_plural = "Registry Entries"

    def __str__(self):
        return self.phagename

    def validate(self, value):
        super(RegistryEntry, self).validate(value)

        if len(value) < 4:
            raise ValidationError("Too short")
        return True

class RegistryEntryForm(ModelForm):
    class Meta:
        model = RegistryEntry
        fields = ['phagename', 'exturl']

class LoginForm(Form):
    username = CharField(label='Username', max_length=100)
    password = CharField(label='Password', max_length=100, widget=PasswordInput)
