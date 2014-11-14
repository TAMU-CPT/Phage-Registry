from django.shortcuts import render
from .models import RegistryEntry
from django.http import HttpResponse, HttpResponseBadRequest
import json
import Levenshtein

# Create your views here.

def registry_list(request):
    registries = RegistryEntry.objects.all()
    return render(request, 'registry/post_list.html', {'entries': registries})

def search_page(request):
    return render(request, 'registry/search.html')

def similar_names(request):

    if 'name' in request.GET:
        entries = RegistryEntry.objects.all()
        objects = []
        for e in entries:
            d = Levenshtein.distance(e.phagename, request.GET['name'])
            if d < 3:
                objects.append({
                    'name': e.phagename,
                    'd': d
                })

        return HttpResponse(json.dumps(objects), content_type='application/json')
    else:
        return HttpResponseBadRequest()
