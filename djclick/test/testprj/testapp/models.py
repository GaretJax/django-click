from __future__ import unicode_literals

from django.db import models
from six import python_2_unicode_compatible


@python_2_unicode_compatible
class DummyModel(models.Model):
    slug = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id)
