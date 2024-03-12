from django.http import JsonResponse, Http404
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.views import View
from account.models import Client
from django.core.serializers.json import DjangoJSONEncoder
import json
from .models import Blog


class Blogs(View):
    def post(self, request):

        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Not Logged In'}, status=404)

        data = json.loads(request.body.decode('utf-8')) 
        title = data.get('title')
        content = data.get('content')
        author_id = data.get('author')
        game = data.get('game')
        
        if not all([title, content, author_id]):
            return JsonResponse({'error': 'Incomplete data provided'}, status=400)
            
        try:
            # Retrieve the Client instance based on author_id
            author = Client.objects.get(pk=author_id)
        except Client.DoesNotExist:
            # Handle case where no Client matches the provided author_id
            return JsonResponse({'error': 'Author not found'}, status=404)

        try:
            blog = Blog.objects.create(
                title=title,
                content=content,
                author=author,  # Pass the Client instance, not the ID
                game=game
            )
            return JsonResponse({'message': 'Blog created successfully'}, status=200)  
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def delete(self, request, pk):

        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Not Logged In'}, status=404)
        
        # Handle DELETE request to delete a specific blog
        try:
            # Attempt to retrieve the blog with the provided primary key
            blog = get_object_or_404(Blog, pk=pk)
            
            #Make sure user that is deleting is the user that created
            if request.user.id != blog.author.id:
                return JsonResponse({'error': 'Account cannot delete blog it did not create'}, status=404)

            # Delete the blog
            blog.delete()
            
            # Return a success message
            return JsonResponse({'message': 'Blog deleted successfully'})
        except Http404:
            return JsonResponse({'error': 'No Primary Key found'}, status=404)
        except Exception as e:
            # Handle any unexpected errors
            return JsonResponse({'error': str(e)}, status=500)
    
    def put(self, request, pk):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Not Logged In'}, status=404)
        
        try:  
            blog = get_object_or_404(Blog, pk=pk)

            if request.user.id != blog.author.id:
                return JsonResponse({'error': 'Account cannot update blog it did not create'}, status=404)
            
            data = json.loads(request.body.decode('utf-8'))
            title = data.get('title')
            content = data.get('content')
            if not all([title, content]):
                return JsonResponse({'error': 'Incomplete data provided'}, status=400)
            blog.title = title
            blog.content = content
            blog.save()
            return JsonResponse({'message': 'Blog updated successfully'})
        except Http404:
            return JsonResponse({'error': 'No Primary Key found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request):
         # Query all blog instances
        blogs = Blog.objects.all()
        
        # Query the 10 newest blog instances, ordered by date posted in descending order
        blogs = Blog.objects.order_by('-date_posted')[:10]

        # Convert each blog instance into a dictionary with only id and title
        blogs_list = list(blogs.values('id', 'title'))
        
        # Return the list as a JSON response
        return JsonResponse({'blogs': blogs_list})
        
class GetBlogs(View):
    def get(self, request, *args, **kwargs):
        # Access query parameters
        filters = request.GET

        if 'id' in filters:
            # If 'id' is provided, fetch the single blog with this ID.
            blog = get_object_or_404(Blog, id=filters['id'])
            blog_data = {
                'id': blog.id,
                'title': blog.title,
                'content': blog.content,
                'date_posted': blog.date_posted.strftime("%Y-%m-%d %H:%M:%S"),
                'author': blog.author.username if blog.author else None,
                'likes': blog.likes,
                'dislikes': blog.dislikes,
                'game': blog.game
            }
            return JsonResponse({'blogs': [blog_data]}, encoder=DjangoJSONEncoder)

        # Filter queryset based on query parameters
        queryset = Blog.objects.all()

        if 'game' in filters:
            queryset = queryset.filter(game=filters['game'])
        if 'author' in filters:
            queryset = queryset.filter(author=filters['author'])
        if 'title' in filters:
            # Perform case-insensitive substring matching on the title field
            queryset = queryset.filter(title__icontains=filters['title'])

        # Order the queryset by date posted
            
        if 'order' in filters:
            if filters['order'] == 'old':
                queryset = queryset.order_by('date_posted')[:10]
            elif filters['order'] == 'likes':
                queryset = queryset.order_by('-likes')[:10]
        else:
            queryset = queryset.order_by('-date_posted')[:10]

        # Convert each blog instance into a dictionary with only id and title
        blogs_list = list(queryset.values('id', 'title'))

        return JsonResponse({'blogs': blogs_list})
        
    def put(self, request, pk):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Not Logged In'}, status=404)
        
        #Update Likes and Dislikes
        try:
            blog = get_object_or_404(Blog, pk=pk)
            data = json.loads(request.body.decode('utf-8'))
            
            action = data.get('action')
            value = data.get('value')
            
            if action == 'like':
                blog.likes += value
                if blog.likes < 0: 
                    blog.likes = 0
            elif action == 'dislike':
                blog.dislikes += value
                if blog.likes < 0: 
                    blog.likes = 0
            else:
                return JsonResponse({'error': 'Invalid action'}, status=400)
            
            blog.save()
            return JsonResponse({'message': f'Blog {action}d successfully', 'likes': blog.likes, 'dislikes': blog.dislikes}, status=200)
        except Blog.DoesNotExist:
            return JsonResponse({'error': 'Blog not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)