import json

from blog.models import Blog
from blog.models import Client as C
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from .models import Favourite as F


class FavouriteBlogsTestCase(TestCase):
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

        payload = {
            "username": "user3",
            "email": "user3@hotmail.com",
            "password": "12345",
            "firstname": "jerry3",
            "lastname": "tom3",
        }

        url = "/account/signup/"
        self.client.post(url, payload, content_type="application/json")

        # Sign in
        sign_in_payload = {"username": "user1", "password": "12345"}
        self.client.post(
            reverse("sign_in"), sign_in_payload, content_type="application/json"
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
        self.client.post(url, payload, content_type="application/json")

        # User2's second blog
        payload = {
            "content": "Stuff for a bloggggg2",
            "title": "My Title2",
            "author": user2_id,
            "game": "Minecraft",
        }

        url = reverse("sign_out")
        self.client.get(url)

    def test_add_favourite_blog(self):
        # Test without Sign in
        user2_id = C.objects.filter(username="user2").first().id
        blog_id = Blog.objects.filter(author=user2_id).first().id
        url = f"/favourite/subscribe/{blog_id}/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        # Sign in as user1
        sign_in_payload = {"username": "user1", "password": "12345"}
        self.client.post(
            reverse("sign_in"), sign_in_payload, content_type="application/json"
        )
        # Favourite user2's blog
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            F.objects.filter(client=C.objects.filter(username="user1").first().id)
            .first()
            .blog.id,
            blog_id,
        )

        # Test with non-exist blog id
        url = f"/favourite/subscribe/100/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_favourite(self):
        user2_id = C.objects.filter(username="user2").first().id
        blog_id = Blog.objects.filter(author=user2_id).first().id
        blog_id_last = Blog.objects.filter(author=user2_id).last().id

        # Sign in as user1
        sign_in_payload = {"username": "user1", "password": "12345"}
        self.client.post(
            reverse("sign_in"), sign_in_payload, content_type="application/json"
        )
        # Favourite user2's first blog
        url = f"/favourite/subscribe/{blog_id}/"
        self.client.post(url)

        # Unsubscribe the user2's first blog
        url = f"/favourite/unsubscribe/{blog_id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

        # Unsubscribe a unfavourite blog
        url = f"/favourite/unsubscribe/{blog_id_last}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 400)

        # Subscribe another blog from user 2
        url = f"/favourite/subscribe/{blog_id}/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

        # Sign out user 1
        self.client.get(reverse("sign_out"))

        # Try unsubscribe
        url = f"/favourite/unsubscribe/{blog_id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
