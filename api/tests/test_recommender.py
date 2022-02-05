from rest_framework.test import APITestCase

from api.recommender.generator import Generator


class RecommenderTests(APITestCase):
    
    def test_generator(self):
        Generator()