from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.views import View
from account.models import Client
import json
from .models import Blog

class Blogs(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8')) 
        title = data.get('title')
        content = data.get('content')
        author_id = data.get('author')
        
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
                author=author  # Pass the Client instance, not the ID
            )
            return JsonResponse({'message': 'Blog created successfully'}, status=200)  
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def delete(self, request, pk):
        # Handle DELETE request to delete a specific blog
        try:
            # Attempt to retrieve the blog with the provided primary key
            blog = get_object_or_404(Blog, pk=pk)
            
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
        try:
            blog = get_object_or_404(Blog, pk=pk)
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
        
        # Convert each blog instance into a dictionary
        blogs_list = list(blogs.values('id', 'title', 'content', 'date_posted', 'author'))
        
        # Return the list as a JSON response
        return JsonResponse({'blogs': blogs_list})
        

class GetBlogs(View):
    def get(self, request, pk):
        try:
            # Attempt to retrieve the specific blog by primary key and convert it into a dictionary
            blog = Blog.objects.filter(pk=pk).values('id', 'title', 'content', 'date_posted', 'author').first()

            # Return the blog as a JSON response
            return JsonResponse(blog)

        except Blog.DoesNotExist:
            return JsonResponse({'error': 'Blog not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)