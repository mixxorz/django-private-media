====================
django-private-media
====================

Overview
--------

By default, uploaded files can be accessed by anyone. This is useful in some
cases like blogs, online stores, etc. But at some point you'll want to have some
files only be accessible to authorized users. You can try hiding or obfuscating
the URLS to these files, but they would still be accessible regardless.
django-private-media helps you add authorization checks before clients can
access certain files.

Attribution
-----------
This is a maintained fork of `RacingTadpole/django-private-media`_.
Key parts of this code are based on code by Stephan Foulis and contributors from
`django-filer`_.

Requirements
------------
Django 1.5 or later.

Quick start
-----------
To upload to a private location, add to your `settings.py` e.g.::

    PRIVATE_MEDIA_URL = '/private/'
    if DEBUG:
        # dev
        import os
        PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
        PRIVATE_MEDIA_ROOT = os.path.join(PROJECT_PATH, 'private')
        PRIVATE_MEDIA_SERVER = 'private_media.servers.DefaultServer'
    else:
        # prod
        PRIVATE_MEDIA_ROOT = '/home/user/my/path/to/private/media'
        PRIVATE_MEDIA_SERVER = 'private_media.servers.ApacheXSendfileServer'
        # PRIVATE_MEDIA_SERVER_OPTIONS = {'arg1': 1, ...}  # (optional) kwargs to init server

The default permissioning is for authenticated staff members to see all, and no one else.
To generalise this, also add::

    PRIVATE_MEDIA_PERMISSIONS = 'myapp.permissions.MyPermissionClass'
    PRIVATE_MEDIA_PERMISSIONS_OPTIONS = {'arg1': 1, ...}  # (optional) kwargs to init

This permissions class must have the method::

    has_read_permission(self, request, path)

which returns True or False.


Add to your `INSTALLED_APPS`::

    INSTALLED_APPS = {
        ...
        'private_media',
        ...
    }


Add to `urls.py`::

    from private_media import urls as private_media_urls

       ...
       url(r'^', include(private_media_urls)),


In your `models.py`, to upload a specific file or image to a private area, use::

    from django.db import models
    from private_media.storages import PrivateMediaStorage

    class Car(models.Model):
        photo = models.ImageField(storage=PrivateMediaStorage())


Because the only information about the file available to the permissions method
is its path, you will need to encode the allowed permissioning into the path on upload.

E.g. you could use this to save the owner's primary key into the path::

    import os
    from django.db import models
    from django.contrib.auth.models import User

    from private_media.storages import PrivateMediaStorage
    def owner_file_name(instance, filename):
        return os.path.join('cars', "{0}".format(instance.user.pk), filename)

    class Car(models.Model):
        owner = models.ForeignKey(User)
        photo = models.ImageField(storage=PrivateMediaStorage(), upload_to=owner_file_name)

And then provide a permissioning class like this (which lets staff and the owner see it)::

    import os
    from django.http import Http404

    class OwnerPkPermissions(object):
        def has_read_permission(self, request, path):
            user = request.user
            if not user.is_authenticated():
                return False
            elif user.is_superuser:
                return True
            elif user.is_staff:
                return True
            else:
                try:
                    owner_pk = int(os.path.split(os.path.split(path)[0])[1])
                except ValueError:
                    raise Http404('File not found')
                return (user.pk==owner_pk)

.. _RacingTadpole/django-private-media: https://github.com/RacingTadpole/django-private-media
.. _django-filer: https://github.com/stefanfoulis/django-filer
