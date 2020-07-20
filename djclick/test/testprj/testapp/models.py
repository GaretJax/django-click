from django.db import models


class DummyModel(models.Model):
    slug = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id)
