from typing import List
from matplotlib import pyplot as plt


def plot_values(values: List[float], title: str) -> None:
    """
    Produce graph given values.
    :param values: List of floats.
    :param title: Graph title.
    """
    plt.xlabel("Student number")
    plt.ylabel("Satisfaction")
    plt.title(title)
    plt.ylim([0, 1])
    plt.scatter(range(len(values)), values, marker="o", s=2)
    plt.savefig(f"api/recommender/plots/{title}.png")
