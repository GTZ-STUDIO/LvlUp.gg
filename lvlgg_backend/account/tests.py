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

    def test_delete_user(self):
        payload = {
            "username": "user1",
            "email": "user1@hotmail.com",
            "password": "12345",
            "firstname": "jerry",
            "lastname": "tom",
        }

        url_post = "/account/signup/"

        for i in range(2):
            payload["username"] = f"user{i}"
            payload["email"] = f"user{i}@hotmail.com"
            self.client.post(url_post, payload, content_type="application/json")

        # Delete a non-exist user
        response = self.client.delete("/account/delete/5/")
        self.assertEqual(response.status_code, 404)

        # Delete first user
        response = self.client.delete("/account/delete/1/")
        self.assertEqual(response.status_code, 200)

        # Delete second user
        response = self.client.delete("/account/delete/2/")
        self.assertEqual(response.status_code, 200)

    def test_get_user(self):
        payload = {
            "username": "user1",
            "email": "user1@hotmail.com",
            "password": "12345",
            "firstname": "jerry",
            "lastname": "tom",
        }
        url_post = "/account/signup/"
        self.client.post(url_post, payload, content_type="application/json")

        response = self.client.get("/account/1/")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["username"], "user1")
        self.assertEqual(data["email"], "user1@hotmail.com")

        response = self.client.get("/account/5/")
        self.assertEqual(response.status_code, 404)
