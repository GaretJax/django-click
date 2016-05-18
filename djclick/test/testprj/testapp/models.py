from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class DummyModel(models.Model):
    def __str__(self):
        return str(self.id)
