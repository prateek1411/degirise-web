import os

from django.db import models

# Create your models here.

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='.')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def get_extension(self):
        name, extension = os.path.splitext(self.document.name)
        return extension

    def get_short_name(self):
        if len(self.document.name) > 10:
            return self.document.name[:9]
        else:
            return self.document.name
