from django.conf.urls import patterns, include, url
from blog.views import archive

urlpatterns = patterns ('',
    url(r'^$', archive),
)