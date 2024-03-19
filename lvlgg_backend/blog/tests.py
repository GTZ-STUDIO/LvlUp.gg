import json

from django.test import TestCase
from django.test.client import Client
from account.models import Client
from blog.models import Blog
from django.urls import reverse

# Create your tests here.

class BlogViewTestCase(TestCase):
    
    def setUp(self):
        # Create a Client instance
        self.client_user = Client.objects.create_user(username="user1", email="user1@example.com", password="testpassword", firstname="Jerry", lastname="Tom")
        # Verify that the Client instance is createds
        self.assertIsNotNone(self.client_user)
        # Verify that the primary key is retrieved correctly
        self.assertIsNotNone(self.client_user.pk)
        # Save the primary key for later use
        self.user_pk = self.client_user.pk

        #Login
        payload = {
            "username" : "user1",
            "password" : "testpassword"
        }

        url = "/account/signin/"

        response = self.client.post(url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)


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
            "author": self.user_pk,
            "game" : "Minecraft"
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
            "author": self.user_pk,
            "game" : "Minecraft"
        }
        create_url = "/blog/create_blog/"
        response = self.client.post(create_url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        # Retrieve list of blogs
        get_url = "/blog/get_blog/"
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
           
        first_blog = blogs[0]
        self.assertEqual(first_blog['title'], payload['title'])

    def test_get_blogs_byId(self):
        """
        Test getting all blogs
        """
        # Retrieve list of blogs
        get_url = f"/blog/get_blog/?id={self.blog_pk}"
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
           
        first_blog = blogs[0]
        self.assertEqual(first_blog['id'], self.blog_pk)

    def test_get_blogs_byTitle(self):
        """
        Test getting all blogs
        """
        # Create a blog first
        payload = {
            "content": "Stuff for a bloggggg",
            "title": "Sample Title Test",
            "author": self.user_pk,
            "game" : "Minecraft"
        }
        create_url = "/blog/create_blog/"
        response = self.client.post(create_url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        # Retrieve list of blogs
        get_url = f"/blog/get_blog/?title=Sample"
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
        self.assertEqual( len(blogs), 2)

        # Retrieve list of blogs
        get_url = f"/blog/get_blog/?title=Sample Title Test"
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
        self.assertEqual( len(blogs), 1)


    def test_get_blogs_byGame(self):
        """
        Test getting all blogs
        """
        # Create a blog first
        payload = {
            "content": "Stuff for a bloggggg",
            "title": "My Title",
            "author": self.user_pk,
            "game" : "Minecraft"
        }
        create_url = "/blog/create_blog/"
        response = self.client.post(create_url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        # Retrieve list of blogs
        get_url = f"/blog/get_blog/?game=Minecraft"
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
           
        first_blog = blogs[0]
        self.assertEqual(first_blog['title'], payload['title'])

    def test_get_blogs_byAuthor(self):
        """
        Test getting all blogs
        """
        # Create a blog first
        payload = {
            "content": "Stuff for a bloggggg",
            "title": "My Title",
            "author": self.user_pk,
            "game" : "Minecraft"
        }
        create_url = "/blog/create_blog/"
        response = self.client.post(create_url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        # Retrieve list of blogs
        get_url = f"/blog/get_blog/?author={self.user_pk}"
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
           
        first_blog = blogs[0]
        self.assertEqual(first_blog['title'], payload['title'])
     
    def test_get_blogs_byOrderOld(self):
        """
        Test getting all blogs
        """
        # Create a blog first
        payload = {
            "content": "Stuff for a bloggggg",
            "title": "My Title",
            "author": self.user_pk,
            "game" : "Minecraft"
        }
        create_url = "/blog/create_blog/"
        response = self.client.post(create_url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        # Retrieve list of blogs
        get_url = f"/blog/get_blog/?order=old"
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
           
        first_blog = blogs[1]
        self.assertEqual(first_blog['title'], payload['title'])

    def test_get_blogs_byOrderLikes(self):
        """
        Test getting all blogs
        """
        # Create a blog first
        payload = {
            "content": "Stuff for a bloggggg",
            "title": "My Title",
            "author": self.user_pk,
            "game" : "Minecraft"
        }
        create_url = "/blog/create_blog/"
        response = self.client.post(create_url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        #Update Likes

        update_url = f"/blog/likes/{self.blog_pk}/"

        update = {
            "action": "like",
            "value": 1,
        }

        response = self.client.put(update_url, update, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        # Retrieve list of blogs
        get_url = f"/blog/get_blog/?order=likes"
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
           
        first_blog = blogs[0]
        self.assertEqual(first_blog['title'], "Sample Blog Post" )

    def test_get_blogs_multiple_filters(self):
        """
        Test getting all blogs
        """
        # Create a blog first
        payload = {
            "content": "Stuff for a bloggggg",
            "title": "My Title",
            "author": self.user_pk,
            "game" : "Minecraft"
        }
        create_url = "/blog/create_blog/"
        response = self.client.post(create_url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        # Retrieve list of blogs
        get_url = f"/blog/get_blog/?order=old&title=My Title&game=Minecraft"
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
           
        first_blog = blogs[0]
        self.assertEqual(first_blog['title'], payload['title'])

    def test_get_blogs_empty(self):
        """
        Test getting all blogs when there are no blogs
        """

        # Retrieve list of blogs
        get_url = "/blog/get_blog/?game=NOTAGAME"
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

    def test_update_likes(self):
        """
        Test updating a blog
        """

        update_url = f"/blog/likes/{self.blog_pk}/"

        update = {
            "action": "like",
            "value": 1,
        }

        response = self.client.put(update_url, update, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        update['action'] = 'dislike'
        response = self.client.put(update_url, update, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        update['action'] = 'like'

        update['amount'] = -1
        response = self.client.put(update_url, update, content_type="application/json")
        self.assertEqual(response.status_code, 200)

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

class reccomended(TestCase):

    def setUp(self):
        # Create a Client instance
        self.client_user = Client.objects.create_user(username="user1", email="user1@example.com", password="testpassword", firstname="Jerry", lastname="Tom")
        self.client_friend = Client.objects.create_user(username="Dave", email="friend1@example.com", password="friendpassword", firstname="Tom", lastname="Cat")
        self.client_extra = Client.objects.create_user(username="Extra", email="extra1@example.com", password="friendpassword", firstname="Random", lastname="Cat")
        # Save the primary key for later use
        self.user_pk = self.client_user.pk
        self.friend_pk = self.client_friend.pk
        self.extra_pk = self.client_extra.pk

        #Login
        payload = {
            "username" : "user1",
            "password" : "testpassword"
        }

        url = "/account/signin/"

        self.client.post(url, payload, content_type="application/json")
        
        #Friend other user
        payload = {
            "username" : "Dave",
        }

        url = "/account/follow/"

        self.client.post(url, payload, content_type="application/json")

        #Make A Blog
        self.blog_post = Blog.objects.create(
            title="Sample Blog Post",
            content="This is a sample blog post content.",
            author=self.client_friend,  
        )
        self.blog_pk = self.blog_post.pk

        #Make A Blog to be saved
        self.blog_post2 = Blog.objects.create(
            title="Saved Blog",
            content="This is a sample blog post content for one that has been saved.",
            author=self.client_extra,  
            game = "Minecraft",
        )
        self.blog_pk2 = self.blog_post2.pk

        self.blog_post2 = Blog.objects.create(
            title="Random Blog",
            content="This is a random blog",
            author=self.client_extra,  
            game = "Minecraft",
        )

        #Save  Blog
        url = f"/favourite/subscribe/{self.blog_pk2}/"

        self.client.post(url, payload, content_type="application/json")

    def test_getReccomended(self):

        url = "/blog/recommended/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


        data = json.loads(response.content.decode('utf-8'))
        # Check if the response contains a 'blogs' key
        self.assertIn('blogs', data)
        # Get the list of blogs from the response
        blogs = data['blogs']
        self.assertEqual( len(blogs), 2)

class reccomended_no_user(TestCase):

    def setUp(self):
        # Create a Client instance
        self.client_user = Client.objects.create_user(username="user1", email="user1@example.com", password="testpassword", firstname="Jerry", lastname="Tom")
        self.client_friend = Client.objects.create_user(username="Dave", email="friend1@example.com", password="friendpassword", firstname="Tom", lastname="Cat")
        self.client_extra = Client.objects.create_user(username="Extra", email="extra1@example.com", password="friendpassword", firstname="Random", lastname="Cat")
        # Save the primary key for later use
        self.user_pk = self.client_user.pk
        self.friend_pk = self.client_friend.pk
        self.extra_pk = self.client_extra.pk
        

        #Make A Blog
        self.blog_post = Blog.objects.create(
            title="Sample Blog Post",
            content="This is a sample blog post content.",
            author=self.client_friend,  
        )

        #Make A Blog to be saved
        self.blog_post2 = Blog.objects.create(
            title="Saved Blog",
            content="This is a sample blog post content for one that has been saved.",
            author=self.client_extra,  
            game = "Minecraft",
        )

        self.blog_post2 = Blog.objects.create(
            title="Random Blog",
            content="This is a random blog",
            author=self.client_extra,  
            game = "Minecraft",
        )

    def test_get_recommended_notuser(self):

        url = "/blog/recommended/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


        data = json.loads(response.content.decode('utf-8'))
        # Check if the response contains a 'blogs' key
        self.assertIn('blogs', data)
        # Get the list of blogs from the response
        blogs = data['blogs']
        self.assertEqual( len(blogs), 3)
























