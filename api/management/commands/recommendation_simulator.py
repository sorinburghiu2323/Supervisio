from api.recommender.generator import Generator
from api.recommender.recommender_engine import LinearRecommender
from api.users.models import User

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Generate dummy data.
    WARNING: It will flush the current database.
    """

    def handle(self, *args, **kwargs):
        print(User.objects.count())
        Generator(100)
        print(2)
        user = User.objects.filter(is_supervisor=False).first()
        print(3)
        recommender = LinearRecommender(user)
        print(4)

        print(recommender.get_project_recommendations())
        print(recommender.get_supervisor_recommendations())
