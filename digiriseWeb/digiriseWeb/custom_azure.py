from datetime import datetime, timedelta

from azure.storage.blob import BlockBlobService, ContainerPermissions
from django.conf import settings
from storages.backends.azure_storage import AzureStorage


class AzureMediaStorage(AzureStorage):
    azure_container = settings.MEDIA_CONTAINER
    location = 'webApp'
    file_overwrite = False