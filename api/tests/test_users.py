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

    def test_get_me(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url + "me/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], self.user.email)

    def test_update_me(self):
        # User is not supervisor.
        self.client.force_authenticate(self.user)
        response = self.client.patch(self.url + "me/")
        self.assertEqual(response.status_code, 403)

        # Update bio of supervisor.
        self.user.is_supervisor = True
        self.user.save()
        response = self.client.patch(self.url + "me/", {"bio": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.bio, "test")
