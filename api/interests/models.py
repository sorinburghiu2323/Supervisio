from django.db import models

from api.models import TimestampedModel


class Interest(TimestampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Interest, self).save(*args, **kwargs)
