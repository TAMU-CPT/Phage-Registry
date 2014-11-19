from django.shortcuts import render, redirect
from .models import RegistryEntry, RegistryEntryForm, LoginForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from haystack.query import SearchQuerySet


import json
import Levenshtein

# Create your views here.

def registry_list(request):
    registries = RegistryEntry.objects.all().order_by('phagename')
    paginator = Paginator(registries, 20)

    page = request.GET.get('page')
    try:
        e = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        e = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        e = paginator.page(paginator.num_pages)

    return render(request, 'registry/post_list.html', {'entries': e})

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
                messages.add_message(request, messages.SUCCESS, 'Entry Saved.')
                form.save()
                return render(request, 'registry/add_phage.html', {'form': form})
            else:
                return render(request, 'registry/add_phage.html', {'form': form})
        else:
            form = RegistryEntryForm()
            return render(request, 'registry/add_phage.html', {'form': form})
    else:
        return redirect('login')

def login_view(request):
    if request.method == 'GET':
        return render(request, 'registry/login.html', {'form': LoginForm()})
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

def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))
    results = [r.pk for r in sqs]
    docs = RegistryEntry.objects.filter(pk__in=results)
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': [{'name': doc.phagename, 'url': doc.exturl, 'alias': doc.alias_list} for doc in docs]
    })
    return HttpResponse(the_data, content_type='application/json')
