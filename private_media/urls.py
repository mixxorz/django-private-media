from django.conf.urls import url
from django.conf import settings

from .views import serve_private_file

urlpatterns = [
    url(r'^{0}(?P<path>.*)$'.format(settings.PRIVATE_MEDIA_URL.lstrip('/')),
        serve_private_file)
]
