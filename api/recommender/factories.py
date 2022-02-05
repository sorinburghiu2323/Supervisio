import factory
from factory.django import DjangoModelFactory
from api.interests.models import Interest
from api.projects.models import Project

from api.users.models import User


class UserFactory(DjangoModelFactory):
    email = factory.Faker("email")

    class Meta:
        model = User


class ProjectFactory(DjangoModelFactory):
    supervisor = factory.SubFactory(UserFactory)

    class Meta:
        model = Project


class InterestFactory(DjangoModelFactory):
    name = factory.Faker("name")

    class Meta:
        model = Interest
