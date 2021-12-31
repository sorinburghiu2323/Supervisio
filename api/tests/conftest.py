from api.users.models import User


def test_user(email="test@example.com"):
    user, created = User.objects.get_or_create(
        email=email,
        first_name="Test",
        last_name="Ing",
    )
    if created:
        user.set_password("Password1")
        user.save()
    return user
