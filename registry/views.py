from django.shortcuts import render, redirect
from .models import RegistryEntry, RegistryEntryForm
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth import authenticate, login
import json
import Levenshtein

# Create your views here.

def registry_list(request):
    registries = RegistryEntry.objects.all().order_by('phagename')
    return render(request, 'registry/post_list.html', {'entries': registries})

def search_page(request):
    return render(request, 'registry/search.html')

def similar_names(request):

    if 'name' in request.GET:
        entries = RegistryEntry.objects.all()
        objects = []
        for e in entries:
            d = Levenshtein.distance(e.phagename, request.GET['name'])
            if d < 4:
                objects.append({
                    'name': e.phagename,
                    'd': d
                })
        return HttpResponse(json.dumps(sorted(objects, key=lambda x: x['d'])), content_type='application/json')
    else:
        return HttpResponseBadRequest()

def add_phage(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            # Pre-populate user id
            re = RegistryEntry(owner_id=request.user.id)
            # Use this as a base for the form data submitted by user
            form = RegistryEntryForm(request.POST, instance=re)
            if form.is_valid():
                form.save()
                return render(request, 'registry/add_phage.html', {'form': form, 'message': "Entry Saved!"})
            else:
                return render(request, 'registry/add_phage.html', {'form': form})
        else:
            form = RegistryEntryForm()
            return render(request, 'registry/add_phage.html', {'form': form})
    else:
        return redirect('login')

def login_view(request):
    if request.method == 'GET':
        return render(request, 'registry/login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/phage-registry/')
            else:
                return redirect('/phage-registry/login')
        else:
            return redirect('/phage-registry/login')
    else:
        return redirect('/phage-registry/login')

def logout_view(request):
    logout(request)
    return redirect('/phage-registry/')
