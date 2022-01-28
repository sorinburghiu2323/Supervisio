from email.mime import application
from rest_framework.test import APITestCase
from api.projects.models import Project, ProjectApplication

from api.tests.conftest import test_application, test_interest, test_project, test_user


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

    def test_get_projects_filter_by_interests(self):
        # No interests.
        response = self.client.get(self.url, {"interests": "[]"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        # Get projects with interests.
        interest = test_interest()
        self.project.interests.add(interest)
        response = self.client.get(self.url, {"interests": f"[{interest.id}]"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_projects_filter_by_supervisors(self):
        # Non existing supervisor.
        response = self.client.get(self.url, {"supervisor": f"{self.user.id + 1}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        # Existing supervisor.
        response = self.client.get(self.url, {"supervisor": f"{self.user.id}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

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

    def test_delete_project(self):
        # A user who is not the project owner cannot delete it.
        invalid_user = test_user(email="test2@example.com")
        self.client.force_authenticate(invalid_user)
        response = self.client.delete(self.url + f"{self.project.id}/")
        self.assertEqual(response.status_code, 403)

        # Project with open application is invalid.
        application = test_application()
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.url + f"{self.project.id}/")
        self.assertEqual(response.status_code, 400)

        # Correct request.
        application.status = "rejected"
        application.save()
        response = self.client.delete(self.url + f"{self.project.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Project.objects.filter(id=self.project.id).exists())

    def test_apply_for_project(self):
        # Supervisors cannot apply to projects.
        self.user.is_supervisor = True
        self.user.save()
        response = self.client.post(self.url + f"{self.project.id}/apply/")
        self.assertEqual(response.status_code, 403)

        # There is already a project application.
        self.user.is_supervisor = False
        self.user.save()
        application = test_application()
        response = self.client.post(self.url + f"{self.project.id}/apply/")
        self.assertEqual(response.status_code, 400)

        # Correct request.
        application.status = "rejected"
        application.save()
        response = self.client.post(
            self.url + f"{self.project.id}/apply/", {"message": "test"}
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            ProjectApplication.objects.filter(
                student=self.user,
                project=self.project,
                status="pending",
                message="test",
            ).exists()
        )


class ProjectApplicationTests(APITestCase):
    def setUp(self) -> None:
        self.url = "/api/projects/applications/"
        self.user = test_user()
        self.application = test_application()
        self.application_2 = test_application(status="approved")
        self.user.is_supervisor = True
        self.user.save()
        self.client.force_authenticate(self.user)

    def test_get_applications(self):
        # Correct request.
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        # Not supervisor.
        self.user.is_supervisor = False
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_get_applications_filter_by_approved(self):
        # Bad request.
        response = self.client.get(self.url, {"is_approved": "bad"})
        self.assertEqual(response.status_code, 400)

        # Filter by not approved.
        response = self.client.get(self.url, {"is_approved": "false"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.application.id)

        # Filter by approved.
        response = self.client.get(self.url, {"is_approved": "true"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.application_2.id)

    def test_review_application(self):
        # No body.
        response = self.client.post(self.url + f"{self.application.id}/review/")
        self.assertEqual(response.status_code, 400)

        # Bad body.
        response = self.client.post(
            self.url + f"{self.application.id}/review/", {"is_approved": "bad"}
        )
        self.assertEqual(response.status_code, 400)

        # Approved application.
        response = self.client.post(
            self.url + f"{self.application.id}/review/", {"is_approved": "true"}
        )
        self.assertEqual(response.status_code, 200)
        self.application = ProjectApplication.objects.get(id=self.application.id)
        self.assertEqual(self.application.status, "approved")

        # Rejected application.
        response = self.client.post(
            self.url + f"{self.application.id}/review/", {"is_approved": "false"}
        )
        self.assertEqual(response.status_code, 200)
        self.application = ProjectApplication.objects.get(id=self.application.id)
        self.assertEqual(self.application.status, "rejected")
