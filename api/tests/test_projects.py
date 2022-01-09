from rest_framework.test import APITestCase

from api.tests.conftest import test_interest, test_project, test_user


class ProjectTests(APITestCase):
    def setUp(self) -> None:
        self.url = "/api/projects/"
        self.user = test_user()
        self.client.force_authenticate(self.user)
        self.project = test_project()
        self.project_2 = test_project("software")

    def test_get_projects(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_projects_filter_by_phrase(self):
        response = self.client.get(self.url, {"phrase": "soft"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_project(self):
        # Students cannot create projects.
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)
        self.user.is_supervisor = True
        self.user.save()

        # No body.
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)

        # Valid request.
        interest = test_interest()
        response = self.client.post(
            self.url,
            {
                "title": "aws integrations",
                "description": "lorem ipsum",
                "interests": [int(interest.id)],
            },
        )
        self.assertEqual(response.status_code, 201)
