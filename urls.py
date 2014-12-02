# urls.py
from django.conf.urls import patterns, url, include
from yaml_def.api import api

urlpatterns = patterns('',
    (r'^api/', include(api.urls)),
)

