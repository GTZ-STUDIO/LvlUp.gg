from django.http import JsonResponse, Http404
from account.models import Client
from blog.models import Blog
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views import View
import json
from .models import Comment

class Comments(View):

    def post(self, request):
        data = json.loads(request.body.decode('utf-8')) 
        content = data.get('content')
        author_id = data.get('author')
        blog_id = data.get('blog')
        
        if not content:
            return JsonResponse({'error': 'Content is required'}, status=400)
            
        try:

            # Retrieve the Client instance based on author_id
            author = Client.objects.get(pk=author_id)
            # Retrieve the Blog instance based on blog_id
            blog = Blog.objects.get(pk=blog_id)

            comment = Comment.objects.create(
                content=content,
                author=author,
                blogId=blog,
            )
            return JsonResponse({'message': 'Comment created successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request, blog_Id):
        comments = Comment.objects.filter(blogId=blog_Id)  
        comments_list = list(comments.values('id','content','date_posted','author','blogId'))
        return JsonResponse({'comments':comments_list})
    

    def delete(self, request, pk):
        try:
            comment = get_object_or_404(Comment, pk=pk)
            comment.delete()
            return JsonResponse({'message': 'Comment deleted successfully'}, status=200)
        except Http404:
            return JsonResponse({'error': 'No Primary Key found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # Assuming you want to update comments as well
    def put(self, request, pk):
        try:
            comment = get_object_or_404(Comment, pk=pk)
            data = json.loads(request.body.decode('utf-8'))
            content = data.get('content')
            if not content:
                return JsonResponse({'error': 'Content is required'}, status=400)
            comment.content = content
            # Optionally update other fields like author or blog if needed
            comment.save()
            return JsonResponse({'message': 'Comment updated successfully'}, status=200)
        except Http404:
            return JsonResponse({'error': 'No Primary Key found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


