from typing import List
from api.grades.models import Grade
from api.projects.models import Project
from api.recommender.utils import calculate_grade_relevance, calculate_interest_match_factor
from api.users.models import User

RECOMMENDED_BEFORE_BIAS = 4


def calculate_recommendation_satisfaction(
    user: User, projects: List[Project], supervisors: List[User]
) -> float:
    """
    Satisfaction calculator based on:
    - interest relation
    - how much it was already recommended

    Output value:
    0 - recommendations are pointless
    1 - recommendations are perfect

    :param user: User instance.
    :param projects: List of recommended projects.
    :param supervisors: List of recommended supervisors.
    :return: Satisfaction score as float.
    """
    user_interests = user.interests.all()
    interests_count = user_interests.count()
    grades = Grade.objects.filter(student=user)
    grade_count = grades.count()

    # Get matches and recommended before count.
    matches = []
    recommended_before = 0
    for project in projects:
        matches.append(
            (calculate_interest_match_factor(user_interests, project) + calculate_grade_relevance(grades, project)) / (interests_count + grade_count)
        )
        recommended_before += project.recommended_count
        project.recommended_count += 1
        project.save()
    for supervisor in supervisors:
        matches.append(
            (calculate_interest_match_factor(user_interests, supervisor) + calculate_grade_relevance(grades, supervisor))
            / (interests_count + grade_count)
        )
        recommended_before += supervisor.recommended_count
        supervisor.recommended_count += 1
        supervisor.save()

    # Add 0's until max.
    for _ in range(6 - len(matches)):
        matches.append(0)

    average_match = sum(matches) / len(matches)
    return (
        average_match
        if recommended_before == 0
        else average_match / (recommended_before ** (1 / RECOMMENDED_BEFORE_BIAS))
    )
