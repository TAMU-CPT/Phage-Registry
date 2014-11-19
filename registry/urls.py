from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.registry_list),
    url(r'^similar/$', views.similar_names),
    url(r'^search/$', views.search_page),
    url(r'^haystack/', include('haystack.urls')),
    url(r'^create/$', views.add_phage),
    url(r'^login/$', views.login_view),
    url(r'^logout/$', views.logout_view),

)

