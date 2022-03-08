import factory
from factory.django import DjangoModelFactory
from api.interests.models import Interest
from api.projects.models import Project
from api.grades.models import Module, Grade

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
    name = factory.Faker("job")

    class Meta:
        model = Interest


class ModuleFactory(DjangoModelFactory):
    name = factory.Faker("job")

    class Meta:
        model = Module


class GradeFactory(DjangoModelFactory):
    student = factory.SubFactory(UserFactory)
    module = factory.SubFactory(ModuleFactory)
    score = factory.Faker("pyint", min_value=0, max_value=100)

    class Meta:
        model = Grade
