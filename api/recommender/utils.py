from typing import List, Tuple
from api.interests.models import Interest

from api.projects.models import Project
from api.users.models import User


def calculate_interest_match_factor(
    user_interests: List[Interest], object: Tuple[Project, User]
) -> int:
    """
    Get score of how well a project/supervisor matches an interest.
    :param project: Project/User instance.
    :return: int.
    """
    return len(list(set(object.interests.all()).intersection(user_interests)))
