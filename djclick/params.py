import click

from django.core.exceptions import ObjectDoesNotExist


class ModelInstance(click.ParamType):
    def __init__(self, qs, lookup="pk"):
        from django.db import models

        if isinstance(qs, type) and issubclass(qs, models.Model):
            qs = qs.objects.all()
        self.qs = qs
        self.name = "{}.{}".format(qs.model._meta.app_label, qs.model.__name__,)
        self.lookup = lookup

    def convert(self, value, param, ctx):
        if value is None:  # NOCOV
            return super(ModelInstance, self).convert(value, param, ctx)
        try:
            return self.qs.get(**{self.lookup: value})
        except ObjectDoesNotExist:
            pass
        # call `fail` outside of exception context to avoid nested exception
        # handling on Python 3
        msg = "could not find {s.name} with {s.lookup}={value}".format(
            s=self, value=value
        )
        self.fail(msg, param, ctx)
