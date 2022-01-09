from rest_framework.test import APITestCase

from api.tests.conftest import test_interest, test_user


class InterestTests(APITestCase):
    def setUp(self) -> None:
        self.url = "/api/interests/"
        self.user = test_user()
        self.interest = test_interest()
        self.interest_2 = test_interest(name="ai")
        self.interest_3 = test_interest(name="math")
        self.user.interests.set([self.interest_2, self.interest_3])
        self.client.force_authenticate(self.user)

    def test_get_interests(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]["id"], self.interest.id)
        self.assertTrue(response.data[1]["is_favourite"])

    def test_get_interests_favourite_filter(self):
        response = self.client.get(self.url, {"is_favourite": "true"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        response = self.client.get(self.url, {"is_favourite": "false"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        # Test bad favourite filter value.
        response = self.client.get(self.url, {"is_favourite": "bad"})
        self.assertEqual(response.status_code, 400)

    def test_create_interest(self):
        # Student attempting to create.
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)
        self.user.is_supervisor = True
        self.user.save()

        # Missing body.
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)

        # New interest.
        response = self.client.post(self.url, {"name": "aco"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "aco")
        self.assertTrue(self.user.interests.filter(id=response.data["id"]).exists())

        # Duplicate interest.
        response = self.client.post(self.url, {"name": "machine learning"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.interest.id)
        self.assertTrue(self.user.interests.filter(id=response.data["id"]).exists())

        # Duplicate interest non case sensitive.
        # User has already marked this interest as favourite in this case.
        response = self.client.post(self.url, {"name": "MACHINE lEarNing"})
        self.assertEqual(response.status_code, 400)

    def test_update_favourite_interests(self):
        # Missing body.
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, 400)

        # Wrong body.
        response = self.client.patch(self.url, {"interests": "bad"})
        self.assertEqual(response.status_code, 400)

        # Correct usage.
        response = self.client.patch(
            self.url,
            {
                "interests": f"[{self.interest.id}, {self.interest_2.id}, {self.interest_3.id}]"
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.interests.count(), 3)
