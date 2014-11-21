from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from . import views

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="registry/post_list.html")),
    url(r'^u/(.*)$', views.reference),
    url(r'^create/$', views.add_phage),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/phage-registry/'}),
    url(r'^about/', TemplateView.as_view(template_name="registry/about.html")),
    url(r'^rules/', TemplateView.as_view(template_name="registry/rules.html")),
    url(r'^list-data/$', views.OrderListJson.as_view(), name='order_list_json'),
    url(r'^search/find/', views.autocomplete),
)
