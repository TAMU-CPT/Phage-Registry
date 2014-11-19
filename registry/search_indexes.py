import datetime
from haystack import indexes
from .models import RegistryEntry


class RegistryentryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    content_auto = indexes.NgramField(use_template=True)

    def get_model(self):
        return RegistryEntry

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

