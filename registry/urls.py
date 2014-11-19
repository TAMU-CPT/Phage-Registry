from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.registry_list),
    url(r'^similar/$', views.similar_names),
    url(r'^u/(.*)$', views.reference),
    url(r'^create/$', views.add_phage),
    url(r'^login/$', views.login_view),
    url(r'^logout/$', views.logout_view),
    url(r'^search/', include('haystack.urls')),
    url(r'^search/find/', views.autocomplete),
    url(r'^about/', views.about),

)

