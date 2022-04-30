from rest_framework.test import APITestCase
from api.interests.models import Interest
from api.projects.models import Project

from api.recommender.generator import Generator
from api.recommender.plot import plot_values
from api.recommender.recommender_engine import DistributedRecommender, LinearRecommender
from api.recommender.satisfaction_calculator import (
    calculate_recommendation_satisfaction,
)
from api.tests.conftest import test_interest, test_project, test_user
from api.users.models import User


class RecommenderTests(APITestCase):
    def test_generator(self):
        Generator(10, 5, 10, 3, 3, 7, 2)
        self.assertEqual(User.objects.filter(is_supervisor=False).count(), 10)
        self.assertEqual(User.objects.filter(is_supervisor=True).count(), 5)
        self.assertEqual(Project.objects.count(), 15)
        self.assertEqual(Interest.objects.count(), 7)
        self.assertTrue(Project.objects.first().interests.count() in [1, 2])
        self.assertTrue(User.objects.first().interests.count() in [1, 2])

    def test_linear_recommender(self):
        interest_1 = test_interest()
        interest_2 = test_interest(name="another")
        interest_3 = test_interest(name="one more")
        project_1 = test_project(interests=[interest_1, interest_2])
        project_2 = test_project(title="another", interests=[interest_2])
        project_3 = test_project(title="one more", interests=[interest_2, interest_3])
        project_4 = test_project(title="last one")
        user = test_user(
            email="another@example.com", interests=[interest_2, interest_3]
        )
        recommender = LinearRecommender(user)
        recommendations = recommender.get_project_recommendations()
        self.assertTrue(
            list(recommendations)
            in [[project_3, project_2, project_1], [project_3, project_1, project_2]]
        )

    # Note: This test is excluded out of the test suite as it takes long to run.
    # Please run this test individually.
    # def test_simulation(self):
    #     Generator(500)
    #     students = User.objects.filter(is_supervisor=False)
    #     satisfaction = []
    #     for user in students:
    #         recommender = LinearRecommender(user)
    #         projects = recommender.get_project_recommendations()
    #         supervisors = recommender.get_supervisor_recommendations()
    #         satisfaction.append(
    #             calculate_recommendation_satisfaction(user, projects, supervisors)
    #         )
    #     plot_values(satisfaction, recommender.name)
