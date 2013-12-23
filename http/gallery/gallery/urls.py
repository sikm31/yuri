from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import *
from django.contrib import admin
from gallery import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'gallery.views.home', name='home'),
    #url(r'^gallery/', include('gallery.urls')),
    #url(r'^%s' % ROOT_URL[1:], include('gallery.real_urls'))
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()