from importlib import import_module
import logging

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404

logger = logging.getLogger(__name__)


def get_class(import_path=None):
    """Largely based on django.core.files.storage's get_storage_class
    """
    from django.core.exceptions import ImproperlyConfigured
    if import_path is None:
        raise ImproperlyConfigured('No class path specified.')
    try:
        dot = import_path.rindex('.')
    except ValueError:
        raise ImproperlyConfigured("{} isn't a module.".format(import_path))
    module, classname = import_path[:dot], import_path[dot + 1:]
    try:
        mod = import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured(
            'Error importing module {}: "{}"'.format(module, e))
    try:
        return getattr(mod, classname)
    except AttributeError:
        raise ImproperlyConfigured('Module "{}" does not define a "{}" class.'.
                                   format(module, classname))


server = get_class(settings.PRIVATE_MEDIA_SERVER)(**getattr(
    settings, 'PRIVATE_MEDIA_SERVER_OPTIONS', {}))

if hasattr(settings, 'PRIVATE_MEDIA_PERMISSIONS'):
    permissions = get_class(settings.PRIVATE_MEDIA_PERMISSIONS)(
        **getattr(settings, 'PRIVATE_MEDIA_PERMISSIONS_OPTIONS', {}))
else:
    from .permissions import DefaultPrivatePermissions
    permissions = DefaultPrivatePermissions()


def serve_private_file(request, path):
    """Serve private files to users with read permission."""

    logger.debug('Serving {0} to {1}'.format(path, request.user))
    if not permissions.has_read_permission(request, path):
        if settings.DEBUG:
            raise PermissionDenied
        else:
            raise Http404('File not found')
    return server.serve(request, path=path)
