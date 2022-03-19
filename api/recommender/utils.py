from typing import List, Tuple
from api.grades.models import Grade
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


def calculate_grade_relevance(
    grades: List[Grade], object: Tuple[Project, User]
) -> float:
    """
    Calculate how relevant a grade is to a project/supervisor.
    :param grades: List of user grades.
    :param object: Project/User instance.
    :return: float.
    """
    total = 0
    for grade in grades:
        total += (
            1
            + len(
                list(
                    set(object.interests.all()).intersection(
                        grade.module.interests.all()
                    )
                )
            )
            * grade.score
            / 100
        )
    return total
