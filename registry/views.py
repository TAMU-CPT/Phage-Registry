from django.shortcuts import render, redirect
from .models import RegistryEntry, RegistryEntryForm
from django.contrib import messages
from django.utils.html import escape
from haystack.query import SearchQuerySet
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.contrib.auth.decorators import login_required


def reference(request, query):
    query = escape(query)
    try:
        found = RegistryEntry.objects.get(phagename=query)
        if found is not None:
            return redirect(found.exturl)
    except:
        return render(request, 'registry/no-redir.html', {'query': query})

@login_required()
def add_phage(request):
    if request.method == 'POST':
        # Pre-populate user id
        re = RegistryEntry(owner_id=request.user.id)
        # Use this as a base for the form data submitted by user
        form = RegistryEntryForm(request.POST, instance=re)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, 'Entry Saved.')
            form.save()
    else:
        form = RegistryEntryForm()

    return render(request, 'registry/add_phage.html', {'form': form})

class OrderListJson(BaseDatatableView):
    # The model we're going to show
    model = RegistryEntry

    # define the columns that will be returned
    columns = ['phagename', 'alias_list']
    order_columns = ['phagename', 'alias_list']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 250

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'phagename':
            if self.request.user.is_authenticated():
                return '<a href="https://cpt.tamu.edu/phage-registry/u/%s">%s</a> [<a href="https://cpt.tamu.edu/phage-registry/admin/registry/registryentry/%s/">Edit</a>]' % (row.phagename, row.phagename, row.pk)
            else:
                return '<a href="https://cpt.tamu.edu/phage-registry/u/%s">%s</a>' % (row.phagename, row.phagename)
        else:
            return super(OrderListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        q = self.request.GET.get('search[value]', "")
        if len(q) > 0:
            sqs = SearchQuerySet().autocomplete(content_auto=q)
            qs = qs.filter(pk__in=[r.pk for r in sqs])
        return qs
