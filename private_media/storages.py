from django.core.files.storage import FileSystemStorage
from django.conf import settings


class PrivateMediaStorage(FileSystemStorage):

    def __init__(self, location=None, base_url=None):
        if location is None:
            location = settings.PRIVATE_MEDIA_ROOT
        if base_url is None:
            base_url = settings.PRIVATE_MEDIA_URL
        return super(PrivateMediaStorage, self).__init__(location, base_url)
