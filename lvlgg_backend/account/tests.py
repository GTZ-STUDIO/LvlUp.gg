import json

from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from .models import Client as C


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

        user_ids = [user.id for user in C.objects.all()]
        for id in user_ids:
            # Delete first user
            response = self.client.delete(f"/account/delete/{id}/")
            self.assertEqual(response.status_code, 200)

        # Delete a non-exist user
        response = self.client.delete("/account/delete/100/")
        self.assertEqual(response.status_code, 404)

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

        user_id = C.objects.first().id
        response = self.client.get(f"/account/{user_id}/")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["username"], "user1")
        self.assertEqual(data["email"], "user1@hotmail.com")

        response = self.client.get("/account/5/")
        self.assertEqual(response.status_code, 404)

    def test_update_user(self):
        payload = {
            "username": "user1",
            "email": "user1@hotmail.com",
            "password": "12345",
            "firstname": "jerry",
            "lastname": "tom",
        }
        url_post = "/account/signup/"
        self.client.post(url_post, payload, content_type="application/json")

        # Test update user's username
        user_id = C.objects.first().id
        url_put = reverse("update", kwargs={"pk": user_id})
        payload["username"] = "new_name"
        response = self.client.put(url_put, payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        user = C.objects.filter(pk=user_id).first()
        self.assertEqual(user.username, "new_name")
        old_password = user.password
        # create another client, and test cannot upate username which is duplicate
        # with others
        payload2 = {
            "username": "user2",
            "email": "user2@hotmail.com",
            "password": "12345",
            "firstname": "jerry",
            "lastname": "tom",
        }
        self.client.post(url_post, payload2, content_type="application/json")

        # Cannot change username that is duplicate with any other users
        payload["username"] = "user2"
        response = self.client.put(url_put, payload, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(user.username, "new_name")

        # test update password for user "new_name"
        payload3 = {"password": "123456"}
        response = self.client.put(url_put, payload3, content_type="application/json")
        # User after update password, password is hashed, but it is different with
        # previouse password
        user = C.objects.filter(username="new_name").first()
        self.assertNotEqual(old_password, user.password)


class SignInTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        payload = {
            "username": "user1",
            "email": "user1@hotmail.com",
            "password": "12345",
            "firstname": "jerry",
            "lastname": "tom",
        }

        url = "/account/signup/"
        self.client.post(url, payload, content_type="application/json")

    def test_sign_in(self):
        payload = {
            "username": "user1",
            "password": "12345",
        }
        url = "/account/signin/"
        response = self.client.post(url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        payload["password"] = "123"
        response = self.client.post(url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 401)

        payload["password"] = ""
        response = self.client.post(url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 400)

        payload["username"] = ""
        response = self.client.post(url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 400)


class ClientListTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_list_of_users(self):
        payload = {
            "username": "user1",
            "email": "user1@hotmail.com",
            "password": "12345",
            "firstname": "jerry",
            "lastname": "tom",
        }
        self.client.post(reverse("sign_up"), payload, content_type="application/json")
        payload["username"] = "user2"
        payload["email"] = "user2@hotmail.com"
        self.client.post(reverse("sign_up"), payload, content_type="application/json")

        response = self.client.get(reverse("user_list"))
        self.assertEqual(response.status_code, 200)

        users = C.objects.all()
        self.assertEqual(len(users), 2)
