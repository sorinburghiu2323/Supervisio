from api.interests.models import Interest
from api.users.models import User


def test_user(email="test@example.com", is_supervisor=False):
    user, created = User.objects.get_or_create(
        email=email,
        first_name="Test",
        last_name="Ing",
        is_supervisor=is_supervisor,
    )
    if created:
        user.set_password("Password1")
        user.save()
    return user


def test_interest(name="machine learning"):
    interest, _ = Interest.objects.get_or_create(name=name)
    return interest
