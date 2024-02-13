from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json

# Create your views here.

def home(request):
    return HttpResponse('This is the Homepage')

def create(request):
    if request.method == 'POST':
        # Parse the JSON data
        data = json.loads(request.body)
        username = data.get('username', '')
        password = data.get('password', '')
        email = data.get('email', '')

        # Print the received data
        print("It Worked!!")

        # Now you can do whatever you need to do with this data
        # For example, you might want to create a new user with this information

        # Assuming you've successfully created the user, you might return a JSON response
        return JsonResponse({'message': 'Account created successfully'})

    # Handle other HTTP methods or render a response if necessary
    return JsonResponse({'error': 'Method not allowed'}, status=405)