import json

from django.test import TestCase
from django.test.client import Client
from account.models import Client
from blog.models import Blog
from comment.models import Comment
from django.urls import reverse

# Create your tests here.

class CommentViewTestCase(TestCase):

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
            author=self.client_user,  
        )
        self.assertIsNotNone(self.blog_post)
        self.assertIsNotNone(self.blog_post.pk)
        self.blog_pk = self.blog_post.pk

        self.comment_post = Comment.objects.create(
            content = "I am the Comment",
            blogId = self.blog_post,
            author = self.client_user
        )
        self.assertIsNotNone(self.comment_post)
        self.assertIsNotNone(self.comment_post.pk)
        self.comment_pk = self.comment_post.pk

    
    def test_post_comment(self):
        """
        Test creating a new comment
        """
        payload = {
            "content": "I am commenting on a post",
            "blog": self.blog_pk,
            "author": self.user_pk
        }

        url = "/comment/create_comment/"

        response = self.client.post(url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        payload['content'] = ''
        response = self.client.post(url, payload, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        payload['content'] = 'I am commenting on a post'

    def test_get_comments(self):
        """
        Test getting all comments for a blog
        """
        url = f"/comment/get_comments/{self.blog_pk}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        comments = json.loads(response.content.decode('utf-8'))['comments']

        self.assertTrue(comments)

        for comment in comments:
            self.assertIn('id', comment)
            self.assertIn('content', comment)
            self.assertIn('author', comment)
            self.assertIn('blogId', comment)

        first_comment = comments[0] 
        expected_content = "I am the Comment"
        self.assertEqual(first_comment['content'], expected_content)
    
    def test_get_comments_empty(self):
        """
        Test getting all comments for a blog when a blog has no comments
        """
        url = f"/comment/delete_comment/{self.comment_pk}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

        url = f"/comment/get_comments/{self.comment_pk}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Parse JSON response
        data = json.loads(response.content.decode('utf-8'))
        
        # Extract comments list
        comments = data.get('comments', [])

        # Check that comments list is empty
        self.assertFalse(comments, "Comments list should be empty")

        # If the comments list is not empty, fail the test
        if comments:
            self.fail("Comments list is not empty")

    def test_update_comment(self):
        """
        Test updating a comment
        """
        update = {
            "content": "I update a comment on a post",
        }

        url = f"/comment/update_comment/{self.comment_pk}/"

        response = self.client.put(url, update, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        update['content'] = ""
        response = self.client.put(url, update, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_update_comment_fail(self):
        """
        Test updating a comment with wrong pk
        """
        update = {
            "content": "I update a comment on a post",
        }
        key = 99
        url = f"/comment/update_comment/{key}/"

        response = self.client.put(url, update, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_delete_comment(self):
        """
        Test deleting a comment
        """

        url = f"/comment/delete_comment/{self.comment_pk}/"

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_comment_fail(self):
        """
        Test deleting a comment with incorrect pk
        """
        key = 99
        url = f"/comment/delete_comment/{key}/"

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
