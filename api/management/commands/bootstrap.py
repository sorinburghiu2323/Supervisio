from django.core.management.base import BaseCommand
from django.core.management import call_command

from api.interests.models import Interest
from api.projects.models import Project
from api.users.models import User


class Command(BaseCommand):
    """
    Generate dummy data.
    WARNING: It will flush the current database.
    """

    def handle(self, *args, **kwargs):
        print("Initializing bootstrap...")
        call_command("flush", "--no-input")  # Erase current database
        generate_admin()
        generate_dummy_data()
        print("Finished.")


def generate_admin():
    User.objects.create_user(
        first_name="Admin",
        last_name="Istrator",
        password="admin",
        email="admin@example.com",
        is_staff=True,
        is_superuser=True,
    )


def generate_dummy_data():
    """
    This is taken from University of Exeter 3rd Year Dissertation
    proposals made by supervisors in academic year 2020-2021.
    """
    # Create interests.
    interests = [
        "climate change",
        "social media",
        "data science",
        "complex networks",
        "human mind",
        "fault detection",
        "machine learning",
        "statistics",
        "modelling",
        "optimisation",
        "networking",
        "knowledge",
    ]
    interests = [Interest.objects.create(name=interest) for interest in interests]

    # Create student.
    student = User.objects.create_user(
        first_name="Igor",
        last_name="Baker",
        email="ib123@exeter.ac.uk",
        password="Pa55w0rd1",
    )
    student.interests.set([interests[5], interests[11], interests[6]])

    # Create supervisors.
    supervisors = [
        "Massimo Stella",
        "Ravi Kumar Pandit",
        "Tinkle Chugh",
        "Chico Camargo",
        "Achim Brucker",
        # "Johan Wahlstrom",
        # "Federico Botta",
        # "David Acreman",
        # "Jacq Christmas",
        # "Johan Wahlstrom",
        # "Anjan Dutta",
        # "Diego Marmsoler",
        # "Wenjie Ruan",
        # "Jia Hu",
        # "Sareh Rowlands",
        # "Alberto Moraglio",
        # "Riccardo Di Clemente",
        # "Matt Collison",
        # "David Wakeling",
        # "Yulei Wu",
        # "Khulood Alyahya",
        # "Rudy Arthur",
        # "Avik Chakraborti",
        # "Mohamed Bader",
        # "Marcos Oliveira",
    ]
    supervisors = [
        User.objects.create_user(
            first_name=supervisor.split()[0],
            last_name=supervisor.split()[-1],
            email=f"{supervisor.replace(' ', '').lower()}@example.com",
            password="Pa55w0rd1",
            is_supervisor=True,
            bio="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        )
        for supervisor in supervisors
    ]

    # Create projects.
    project = Project.objects.create(
        supervisor=supervisors[0],
        title="Investigating discourse in social media around climate change with data science and language processing",
        description="Climate change is a critical challenge where cognitive and social interactions can greatly hamper or promote concrete interventions. This project aims at reviewing data science and natural language processing approaches for reconstructing how different groups of people report and discuss climate change. The data analysis for this project will adopt co-occurrence networks for testing how social media users discussed the #FridaysForFuture movement (dataset provided by the lecturer). Particular attention will be devoted to using computer science techniques for reconstructing the specific emotions surrounding 'climate change' in social media.",
    )
    project.interests.set([interests[0], interests[1], interests[2]])
    project = Project.objects.create(
        supervisor=supervisors[0],
        title="Using complex networks for exploring the structure of mental walks in the human mind",
        description=(
            "The human mind can store tens of thousands of concepts/ideas in an associative way, so that recalling one concept can also activate other related ideas. The recently released dataset “Small World of Words” captures these memory patterns, free of any specific definition, as a complex network of almost 50k words and over 400k links. "
        ),
    )
    project.interests.set([interests[3], interests[4]])
    project = Project.objects.create(
        supervisor=supervisors[1],
        title="Wind Turbine Fault Detection Using data-driven techniques",
        description="In this project, student apply his/her machine learning skills to solve real world wind turbine industry problems. The datasets will be provided and there is great oppurtunity as well to collaborate/engage with external parnters",
    )
    project.interests.set([interests[2], interests[5]])
    project = Project.objects.create(
        supervisor=supervisors[1],
        title="Image-Based failure data generation based on given articles",
        description="In this project, student apply his/her machine learning skills to solve real world wind turbine industry problems. The datasets will be provided and there is great oppurtunity as well to collaborate/engage with external parnters",
    )
    project.interests.set([interests[2], interests[5]])
    project = Project.objects.create(
        supervisor=supervisors[2],
        title="Comparison of Bayesian Models – Machine Learning Going Back to Roots of Statistics Modelling",
        description="Many statistical models especially Gaussian processes have been widely used for modelling (for both regression and classification) because of their ability to provide uncertainty in predictions in addition to point predictions. Many modern machine learning models e.g., neural networks and random forests have been popular, but they do not provide uncertainty in predictions. In this project, you will compare Bayesian machine learning models especially Bayesian neural networks, Bayesian random forests and Gaussian processes on the given data set. You will use theory of Bayesian statistics and apply it on neural networks and random forest. You will also validate these models on the unseen data set. Contact the supervisor if you want to discuss about the project and refer to the following papers about Bayesian neural networks and Bayesian random forest:",
    )
    project.interests.set([interests[6], interests[7], interests[8]])
    project = Project.objects.create(
        supervisor=supervisors[2],
        title="Machine Learning and Optimisation to Engineering Problems",
        description="Many real-world problems involve computationally expensive and costly experiments. For instance, problems involving computational fluid dynamics (CFD) simulation usually take substantial amount of time for one evaluation. Surrogate-assisted optimisation methods e.g., Bayesian optimisation have been used to solve such kinds of problems to alleviate the computation time. In this project, you will apply and compare different surrogate-assisted optimisation methods especially Bayesian optimisation methods on computational fluid dynamics and benchmark problems. Moreover, you will have the opportunity to apply these methods to problems with multiple objectives. To be summarised, the project will be aimed at finding an optimal solution in least number of evaluations. Please, contact the supervisor for a discussion about the project and refer to the following papers for more details about Bayesian optimisation:",
    )
    project.interests.set([interests[6], interests[9]])
    project = Project.objects.create(
        supervisor=supervisors[3],
        title="Networked narratives, framing and culture wars",
        description="Narratives are the stories we tell about the world. They are the way we connect new information to our preexisting beliefs and opinions. For instance, two people might read the same news article about how the government handled an important issue, and one might say the article shows how their government is incompetent, while the other person might say the article is biased, and their government is actually doing a fantastic job. Both might interpret the article differently, each reinforcing different combinations of beliefs and opinions they might hold -- and ultimately, different sets of narratives -- about the world.",
    )
    project.interests.set([interests[10]])
    project = Project.objects.create(
        supervisor=supervisors[3],
        title="Pandemic science and the construction of knowledge",
        description="Keeping up with the scientific literature on any field is usually a very difficult task. In 2020, this became particularly true for scholars trying to understand the COVID-19 pandemic.",
    )
    project.interests.set([interests[4], interests[11]])
    project = Project.objects.create(
        supervisor=supervisors[4],
        title="Organising Dependencies in Teaching Material",
        description="Teaching material can come in various forms, i.e., texts for self-study, pre-recorded videos, exercises (which might have solutions). There are various relations between these different types of teaching material, e.g., an exercise might only make sense if, beforehand, a certain text of video has been studied.",
    )
    project.interests.set([interests[11], interests[9]])
    project = Project.objects.create(
        supervisor=supervisors[4],
        title="Detecting Malicious Visual Studio Code Extension",
        description="Teaching material can come in various forms, i.e., texts for self-study, pre-recorded videos, exercises (which might have solutions). There are various relations between these different types of teaching material, e.g., an exercise might only make sense if, beforehand, a certain text of video has been studied.",
    )
    project.interests.set([interests[2], interests[6]])
