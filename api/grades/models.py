from api.models import TimestampedModel

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Module(TimestampedModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    interests = models.ManyToManyField("interests.Interest", blank=True)

    def __str__(self):
        return f"[{self.code}] {self.name}"


class Grade(TimestampedModel):
    student = models.ForeignKey("users.User", on_delete=models.CASCADE)
    module = models.ForeignKey("grades.Module", on_delete=models.CASCADE)
    score = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )

    def __str__(self):
        return f"{self.student} - ({self.score}) {self.module}"

    class Meta:
        unique_together = ("student", "module")
