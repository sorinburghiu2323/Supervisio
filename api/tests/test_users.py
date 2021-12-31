from rest_framework.test import APITestCase

from api.tests.conftest import test_user


class UserTests(APITestCase):
    def setUp(self) -> None:
        self.url = "/api/users/"
        self.user = test_user()

    def test_login_and_logout(self):
        # Test user can login.
        response = self.client.post(
            self.url + "login/",
            {
                "email": "test@example.com",
                "password": "Password1",
            },
        )
        self.assertEqual(response.status_code, 200)
        token = response.data["token"]
        self.assertTrue("Token" in token)

        # Test user can logout.
        response = self.client.post(self.url + "logout/", HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 200)

    def test_login_wrong_password(self):
        response = self.client.post(
            self.url + "login/",
            {
                "email": "test@example.com",
                "password": "wrong",
            },
        )
        self.assertEqual(response.status_code, 401)
