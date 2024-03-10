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

        payload["email"] = "wrong_format"
        response = self.client.post(url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_delete_user(self):
        payload = {
            "username": "user1",
            "email": "user1@hotmail.com",
            "password": "12345",
            "firstname": "jerry",
            "lastname": "tom",
        }

        url_post = "/account/signup/"
        self.client.post(url_post, payload, content_type="application/json")

        payload = {"username": "user1", "password": "12345"}
        self.client.post(reverse("sign_in"), payload, content_type="application/json")

        user_id = C.objects.all()
        # Delete first user
        response = self.client.delete(f"/account/delete/{user_id}/")

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

        payload = {"username": "user1", "password": "12345"}
        self.client.post(reverse("sign_in"), payload, content_type="application/json")

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

        # Sign in
        payload = {"username": "user1", "password": "12345"}
        self.client.post(reverse("sign_in"), payload, content_type="application/json")

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
        # Sign in
        payload = {"username": "new_name", "password": "12345"}
        self.client.post(reverse("sign_in"), payload, content_type="application/json")
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

    def test_sign_out(self):

        # User Sign in
        payload = {
            "username": "user1",
            "password": "12345",
        }
        url = "/account/signin/"
        response = self.client.post(url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        url = reverse("sign_out")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.user.is_authenticated, False)


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


class FollowFriendTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create users to add friend
        payload = {
            "username": "user1",
            "email": "user1@hotmail.com",
            "password": "12345",
            "firstname": "jerry",
            "lastname": "tom",
        }

        url = "/account/signup/"
        self.client.post(url, payload, content_type="application/json")

        payload = {
            "username": "user2",
            "email": "user2@hotmail.com",
            "password": "12345",
            "firstname": "jerry2",
            "lastname": "tom2",
        }

        url = "/account/signup/"
        self.client.post(url, payload, content_type="application/json")

    def test_add_friend(self):
        # Without sign in a client
        add_friend_payload = {"username": "user2"}
        response = self.client.post(
            reverse("add_friend"), add_friend_payload, content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)
        # Add user 2 as a friend of user 1
        sign_in_payload = {"username": "user1", "password": "12345"}
        self.client.post(
            reverse("sign_in"), sign_in_payload, content_type="application/json"
        )
        add_friend_payload = {"username": "user2"}
        response = self.client.post(
            reverse("add_friend"), add_friend_payload, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        # Add non exist client
        add_friend_payload["username"] = "none_exist_name"
        response = self.client.post(
            reverse("add_friend"), add_friend_payload, content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)


class RemoveFriendTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create users to add friend
        payload = {
            "username": "user1",
            "email": "user1@hotmail.com",
            "password": "12345",
            "firstname": "jerry",
            "lastname": "tom",
        }

        url = "/account/signup/"
        self.client.post(url, payload, content_type="application/json")

        payload = {
            "username": "user2",
            "email": "user2@hotmail.com",
            "password": "12345",
            "firstname": "jerry2",
            "lastname": "tom2",
        }

        url = "/account/signup/"
        self.client.post(url, payload, content_type="application/json")

        # Sign in
        sign_in_payload = {"username": "user1", "password": "12345"}
        self.client.post(
            reverse("sign_in"), sign_in_payload, content_type="application/json"
        )

        # Add friend
        add_friend_payload = {"username": "user2"}
        self.client.post(
            reverse("add_friend"), add_friend_payload, content_type="application/json"
        )

    def test_remove_friend(self):

        remove_friend_payload = {"username": "user2"}
        response = self.client.post(
            reverse("remove_friend"),
            remove_friend_payload,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        remove_friend_payload = {"username": "user0"}
        response = self.client.post(
            reverse("remove_friend"),
            remove_friend_payload,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)


class FriendListTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        # Create users to add friend
        payload = {
            "username": "user1",
            "email": "user1@hotmail.com",
            "password": "12345",
            "firstname": "jerry",
            "lastname": "tom",
        }

        url = "/account/signup/"
        self.client.post(url, payload, content_type="application/json")

        payload = {
            "username": "user2",
            "email": "user2@hotmail.com",
            "password": "12345",
            "firstname": "jerry2",
            "lastname": "tom2",
        }

        url = "/account/signup/"
        self.client.post(url, payload, content_type="application/json")

        # Sign in
        sign_in_payload = {"username": "user1", "password": "12345"}
        self.client.post(
            reverse("sign_in"), sign_in_payload, content_type="application/json"
        )

        # Add friend
        add_friend_payload = {"username": "user2"}
        self.client.post(
            reverse("add_friend"), add_friend_payload, content_type="application/json"
        )

    def test_get_list(self):
        response = self.client.get(reverse("friend_list"))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]["username"], "user2")


class FriendBlogsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create users to add friend
        payload = {
            "username": "user1",
            "email": "user1@hotmail.com",
            "password": "12345",
            "firstname": "jerry",
            "lastname": "tom",
        }

        url = "/account/signup/"
        self.client.post(url, payload, content_type="application/json")

        payload = {
            "username": "user2",
            "email": "user2@hotmail.com",
            "password": "12345",
            "firstname": "jerry2",
            "lastname": "tom2",
        }

        url = "/account/signup/"
        self.client.post(url, payload, content_type="application/json")

        # Sign in
        sign_in_payload = {"username": "user1", "password": "12345"}
        self.client.post(
            reverse("sign_in"), sign_in_payload, content_type="application/json"
        )

        # Add friend
        add_friend_payload = {"username": "user2"}
        self.client.post(
            reverse("add_friend"), add_friend_payload, content_type="application/json"
        )

        # Sign in user 2
        sign_in_payload = {"username": "user2", "password": "12345"}
        self.client.post(
            reverse("sign_in"), sign_in_payload, content_type="application/json"
        )
        # user2 post blog
        user2_id = C.objects.filter(username="user2").first().id
        payload = {
            "content": "Stuff for a bloggggg",
            "title": "My Title",
            "author": user2_id,
            "game": "Minecraft",
        }

        url = "/blog/create_blog/"

        response = self.client.post(url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        url = reverse("sign_out")
        self.client.get(url)

    def test_get_friend_blogs(self):

        # Test without log in
        friend_name = "user2"
        url = f"/account/friend/{friend_name}/blogs"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # Sign in as user1
        sign_in_payload = {"username": "user1", "password": "12345"}
        self.client.post(
            reverse("sign_in"), sign_in_payload, content_type="application/json"
        )

        # Check friend user2's posts
        friend_name = "user2"
        url = f"/account/friend/{friend_name}/blogs"
        response = self.client.get(url)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "My Title")

        # Check an user that is not a friend
        friend_name = "test_name"
        url = f"/account/friend/{friend_name}/blogs"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
