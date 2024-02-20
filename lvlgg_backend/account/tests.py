import json

from django.test import TestCase
from django.test.client import Client

from .views import ClientDetailView, ClientListView, SignInView


# Create your tests here.
class ClientDetailTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_sign_up(self):
        """
        Test sign up a new user
        """
        payload = {
            "username": "user1",
            "email": "user1@hotmail.com",
            "password": "12345",
            "firstname": "jerry",
            "lastname": "tom",
        }

        url = "/account/signup/"

        response = self.client.post(url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        payload["username"] = ""
        response = self.client.post(url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        payload["username"] = "user1"

        payload["password"] = ""
        response = self.client.post(url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        payload["password"] = "1234"

        payload["email"] = ""
        response = self.client.post(url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        payload["email"] = "user1@hotmail.com"

        payload["firstname"] = ""
        response = self.client.post(url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        payload["firstname"] = "jerry"

        payload["lastname"] = ""
        response = self.client.post(url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        payload["lastname"] = "tom"
