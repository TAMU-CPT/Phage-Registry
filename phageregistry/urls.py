from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns2 = patterns('',
    # Examples:
    #url(r'^$', 'phageregistry.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('registry.urls')),
)

urlpatterns = patterns('',
    url(r'^phage-registry/', include(urlpatterns2))
)
