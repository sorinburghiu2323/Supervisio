from api.interests.models import Interest
from api.projects.models import Project, ProjectApplication
from api.users.models import User


def test_user(email="test@example.com", is_supervisor=False, interests=None):
    user, created = User.objects.get_or_create(
        email=email,
        first_name="Test",
        last_name="Ing",
        is_supervisor=is_supervisor,
    )
    if created:
        user.set_password("Password1")
        user.save()
        if interests:
            user.interests.set(interests)
    return user


def test_interest(name="machine learning"):
    interest, _ = Interest.objects.get_or_create(name=name)
    return interest


def test_project(title="aco", interests=None):
    project, created = Project.objects.get_or_create(
        title=title,
        supervisor=test_user(),
    )
    if created and interests:
        project.interests.set(interests)
    return project


def test_application(status="pending"):
    application, _ = ProjectApplication.objects.get_or_create(
        student=test_user(),
        project=test_project(),
        status=status,
    )
    return application
