from django.shortcuts import render
from django.http import HttpResponseBadRequest, Http404
from django.views import View
import json
from .models import Client
from rest_framework.response import Response
from .serializer import ClientSerializer
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


class SignUpView(APIView):
    def post(self, request):

        data = json.loads(request.body.decode("utf-8"))
        print(data)
        username = data.get("username")
        passowrd = data.get("password")
        email = data.get("email")

        # User or email exist in the db already, refuse registration
        if (
            Client.objects.filter(username=username).exists()
            or Client.objects.filter(email=email).exists()
        ):
            return Response(
                status=400,
                data={"error": "client and email already exist"},
            )

        Client.objects.create_user(username=username, password=passowrd, email=email)
        return Response(
            status=200,
            data={"success": f"client {username} created"},
        )


class UserListView(APIView):
    def get(self, request):
        users = Client.objects.all()
        serializer = ClientSerializer(users, many=True)
        return Response(serializer.data)
