import json

from django.test import TestCase
from django.test.client import Client
from account.models import Client
from blog.models import Blog

# Create your tests here.

class BlogViewTestCase(TestCase):
    
    def setUp(self):
        # Create a Client instance
        self.client_user = Client.objects.create(username="user1", email="user1@example.com", password="testpassword", firstname="Jerry", lastname="Tom")
        # Verify that the Client instance is created
        self.assertIsNotNone(self.client_user)
        # Verify that the primary key is retrieved correctly
        self.assertIsNotNone(self.client_user.pk)
        # Save the primary key for later use
        self.user_pk = self.client_user.pk

        self.blog_post = Blog.objects.create(
            title="Sample Blog Post",
            content="This is a sample blog post content.",
            author=self.client_user,  # Use the previously created Client instance as the author
        )
        self.assertIsNotNone(self.blog_post)
        self.assertIsNotNone(self.blog_post.pk)
        self.blog_pk = self.blog_post.pk


    def test_post_blog(self):
        """
        Test creating a new blog
        """
        payload = {
            "content": "Stuff for a bloggggg",
            "title": "My Title",
            "author": self.user_pk
        }

        url = "/blog/create_blog/"

        response = self.client.post(url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        payload['title'] = ""
        response = self.client.post(url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        payload['title'] = "My title"

        payload['content'] = ""
        response = self.client.post(url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        payload['content'] = "Stuff for my bloggggg"

        payload['author'] = 1000000
        response = self.client.post(url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_get_blogs(self):
        """
        Test getting all blogs
        """
        # Create a blog first
        payload = {
            "content": "Stuff for a bloggggg",
            "title": "My Title",
            "author": self.user_pk
        }
        create_url = "/blog/create_blog/"
        response = self.client.post(create_url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        # Retrieve list of blogs
        get_url = "/blog/getlist/"
        response = self.client.get(get_url)

        # Check response status code
        self.assertEqual(response.status_code, 200)

        # Parse JSON response
        data = json.loads(response.content.decode('utf-8'))

        # Check if the response contains a 'blogs' key
        self.assertIn('blogs', data)

        # Get the list of blogs from the response
        blogs = data['blogs']

        # Check if the returned list is not empty
        self.assertTrue(blogs)

        # Check the structure of each blog in the list
        for blog in blogs:
            self.assertIn('id', blog)
            self.assertIn('title', blog)
            self.assertIn('content', blog)
            self.assertIn('date_posted', blog)
            self.assertIn('author', blog)

        first_blog = blogs[1]
        self.assertEqual(first_blog['content'], payload['content'])
        self.assertEqual(first_blog['title'], payload['title'])
        self.assertEqual(first_blog['author'], payload['author'])

    def test_get_blogs_empty(self):
        """
        Test getting all blogs when there are no blogs
        """
        url = f"/blog/delete_blog/{self.blog_pk}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

        # Retrieve list of blogs
        get_url = "/blog/getlist/"
        response = self.client.get(get_url)

        # Check response status code
        self.assertEqual(response.status_code, 200)

        # Parse JSON response
        data = json.loads(response.content.decode('utf-8'))

        # Check if the response contains a 'blogs' key
        self.assertIn('blogs', data)

        # Get the list of blogs from the response
        blogs = data['blogs']

        # Check if the returned list is empty
        self.assertFalse(blogs)  # or self.assertEqual(len(blogs), 0) as an alternative

    def test_update_blog(self):
        """
        Test updating a blog
        """

        update_url = f"/blog/update_blog/{self.blog_pk}/"

        update = {
            "content": "I updated the blog guys",
            "title": "My Title V2",
        }

        response = self.client.put(update_url, update, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        update['content'] = ''
        response = self.client.put(update_url, update, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        update['content'] = 'I updated the blog Guys'

        update['title'] = ''
        response = self.client.put(update_url, update, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        update['title'] = 'My Title V2'

    def test_update_blog_fail(self):
        """
        Test updating a blog when using a bad pk
        """
        key = 99
        update_url = f"/blog/update_blog/{key}/"

        update = {
            "content": "I updated the blog guys",
            "title": "My Title V2",
        }

        response = self.client.put(update_url, update, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_specific_get(self):
        """
        Test getting a specific blog
        """
        get_url = f"/blog/get_blog/{self.blog_pk}/"
        response = self.client.get(get_url)

        # Check response status code
        self.assertEqual(response.status_code, 200)

        # Parse JSON response
        data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(data['content'], "This is a sample blog post content.")
        self.assertEqual(data['title'], "Sample Blog Post")

        get_url = "/blog/get_blog/99/"
        response = self.client.get(get_url)

        # Check response status code
        self.assertEqual(response.status_code, 500)

    def test_delete(self):
        """
        Test deleting a specific blog
        """
        url = f"/blog/delete_blog/{self.blog_pk}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_fail(self):
        """
        Test Deleting a specific blog a bad pk
        """
        key = 99
        url = f"/blog/delete_blog/{key}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
