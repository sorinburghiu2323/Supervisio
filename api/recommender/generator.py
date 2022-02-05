from typing import List
from django.db import IntegrityError, transaction

import random

from api.interests.models import Interest
from api.projects.models import Project
from api.recommender.factories import InterestFactory, ProjectFactory, UserFactory
from api.users.models import User


class Generator:
    """
    Generate dummy data for testing.
    """

    def __init__(
        self,
        students_num: int = 1000,
        supervisors_num: int = 50,
        projects_per_supervisor: int = 5,
        interests_num: int = 100,
        max_assigned_interests: int = 3,
    ) -> None:
        self.students_num = students_num
        self.supervisors_num = supervisors_num
        self.projects_per_supervisor = projects_per_supervisor
        self.interests_num = interests_num
        self.max_assigned_interests = max_assigned_interests
        self.generate_dummy_data()

    def generate_dummy_data(self):
        # Create interests.
        interests = []
        for _ in range(self.interests_num):
            interests.append(self.generate_interest())

        # Create users.
        students = []
        for _ in range(self.students_num):
            students.append(self.generate_user(interests))
        supervisors = []
        for _ in range(self.supervisors_num):
            supervisors.append(self.generate_user(interests, is_supervisor=True))

        # Create projects for supervisors.
        for supervisor in supervisors:
            for _ in range(self.projects_per_supervisor):
                self.generate_project(supervisor, interests)

    def generate_user(self, interests, is_supervisor: bool = False) -> User:
        """
        Generate dummy user.
        It receives random number from `max_assigned_interests` of random interests
        from the `interests` parameter.
        :param interests: List of Interest instances to choose from.
        :param is_supervisor: (Optional) Make user supervisor.
        :return: User instance.
        """
        while True:
            try:
                with transaction.atomic():
                    user = UserFactory()
                if is_supervisor:
                    user.is_supervisor = True
                    user.save()
                user.interests.set(
                    random.sample(
                        interests, random.randint(1, self.max_assigned_interests)
                    )
                )
                return user
            except IntegrityError:
                continue

    def generate_interest(self) -> Interest:
        """
        Generate factory interest.
        :return: Interest instance.
        """
        while True:
            try:
                with transaction.atomic():
                    return InterestFactory()
            except IntegrityError:
                continue

    def generate_project(self, supervisor: User, interests: List[Interest]) -> Project:
        """
        Generate project for supervisor given interests.
        :param supervisor: User instance.
        :param interests: Interest queryset.
        :return: Project instance.
        """
        project = ProjectFactory(supervisor=supervisor)

        # Give the project a supervisor's interest.
        project.interests.add(random.choice(supervisor.interests.all()))

        # Give the project the rest of the random interests.
        for _ in range(self.max_assigned_interests - 1):
            project.interests.add(random.choice(interests))

        return project
