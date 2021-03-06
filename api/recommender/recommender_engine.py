import random
from typing import List, Tuple
from api.grades.models import Grade
from api.projects.models import Project
from api.recommender.utils import (
    calculate_grade_relevance,
    calculate_interest_match_factor,
)
from api.users.models import User


class BaseRecommender:
    """
    Abstract class to implement project and supervisor recommendations.
    Consits of reusable functions that can be used throughout any approach.
    Please check the jupyter notebook for the implementation of the content-based
    and collaborative-filtering methods.
    """

    name = "Base recommender"

    def __init__(self, user: User) -> None:
        self.user = user
        self.user_interests = user.interests.all()
        self.grades = Grade.objects.filter(student=self.user)

    def get_project_recommendations(self):
        raise NotImplementedError()

    def get_supervisor_recommendations(self):
        raise NotImplementedError()

    def _calculate_grade_relevance(self, object: Tuple[Project, User]) -> float:
        total = 0
        for grade in self.grades:
            total += (
                len(
                    list(
                        set(object.interests.all()).intersection(
                            grade.module.interests.all()
                        )
                    )
                )
                * grade.score
            )
        return total

    def _order_linearly(self, queryset: List, weights: List[float]) -> List:
        """
        Order queryset based on weights linearly.
        :param queryset: Queryset to be ordered.
        :param weights: Weights according to queryset.
        :return: Ordered queryset.
        """
        queryset_weights = list(zip(weights, queryset))
        return [
            x
            for _, x in sorted(queryset_weights, key=lambda x: int(x[0]), reverse=True)
        ]

    def _weighted_shuffle(self, items: list, weights: List[float]):
        """
        Weighted Random Sampling (2005; Efraimidis, Spirakis), complexity: O(n log(n)).
        Algorithm to shuffle list given a list of corresponding weights.
        :param items: items to shuffle as list.
        :param weights: list of corresponding probability.
        :return: shuffled list biased by probability.
        """
        order = sorted(
            range(len(items)), key=lambda i: -random.random() ** (1.0 / weights[i])
        )
        return [items[i] for i in order]


class LinearRecommender(BaseRecommender):
    name = "Linear recommender"

    def __get_recommendations(self, model: Tuple[Project, User]) -> List:
        """
        Get recommendations calculating liner factor relevance.
        :param model: Either Project or User.
        :return: List of recommendations.
        """
        if model == User:
            instances = model.objects.filter(is_supervisor=True)
        else:
            instances = model.objects.all()
        instances = instances.filter(interests__in=list(self.user_interests)).distinct()
        relevance = []
        for instance in instances:
            relevance.append(
                calculate_interest_match_factor(self.user_interests, instance)
                + calculate_grade_relevance(self.grades, instance)
            )
        return self._order_linearly(instances, relevance)[:3]

    def get_supervisor_recommendations(self):
        return self.__get_recommendations(User)

    def get_project_recommendations(self):
        return self.__get_recommendations(Project)


class DistributedRecommender(BaseRecommender):
    name = "Linear distributed recommender"

    def __get_recommendations(self, model: Tuple[Project, User]) -> List:
        """
        Get recommendations using a weighted shuffle approach.
        :param model: Either Project or User.
        :return: List of recommendations.
        """
        if model == User:
            instances = model.objects.filter(is_supervisor=True)
        else:
            instances = model.objects.all()
        instances = instances.filter(interests__in=list(self.user_interests)).distinct()
        relevance = []
        for instance in instances:
            relevance.append(
                calculate_interest_match_factor(self.user_interests, instance)
                + calculate_grade_relevance(self.grades, instance)
            )
        return self._weighted_shuffle(instances, relevance)[:3]

    def get_supervisor_recommendations(self):
        return self.__get_recommendations(User)

    def get_project_recommendations(self):
        return self.__get_recommendations(Project)
