from django.db import models

from api.models import TimestampedModel


class Project(TimestampedModel):
    supervisor = models.ForeignKey("users.User", on_delete=models.CASCADE)
    interests = models.ManyToManyField("interests.Interest", blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    views = models.IntegerField(default=0)
    recommended_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.supervisor.email} - {self.title}"

    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)
        # Update supervisor interests.
        supervisor_projects = Project.objects.filter(supervisor=self.supervisor)
        interests = []
        for project in supervisor_projects:
            interests.extend(list(project.interests.all()))
        self.supervisor.interests.set(interests)


class ProjectApplication(TimestampedModel):
    class ApplicationStatus(models.TextChoices):
        PENDING = "pending"
        APPROVED = "approved"
        REJECTED = "rejected"

    student = models.ForeignKey("users.User", on_delete=models.CASCADE)
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=31,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.PENDING,
    )

    def __str__(self):
        return f"{self.student.email} - {self.project.title}"
