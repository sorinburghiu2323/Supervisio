from django.db import models
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from api.models import TimestampedModel


class Interest(TimestampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        try:
            self.validate_unique()
        except ValidationError:
            raise DRFValidationError({"detail": "Name must be unique."})
        return super(Interest, self).save(*args, **kwargs)
