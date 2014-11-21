from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.registry_list),
    url(r'^u/(.*)$', views.reference),
    url(r'^create/$', views.add_phage),
    url(r'^login/$', views.login_view),
    url(r'^logout/$', views.logout_view),
    url(r'^about/', views.about),
    url(r'^list-data/$', views.OrderListJson.as_view(), name='order_list_json'),
)

