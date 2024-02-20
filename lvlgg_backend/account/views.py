import json

from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Client
from .serializer import ClientSerializer

# Create your views here.


class ClientDetailView(APIView):
    # TODO: update user info, delete a user.testing
    def post(self, request):
        """User sign up

        Args:
            request (Post): with username, password, firstname
                            lastname, email. email and username
                            cannot be duplicate

        Returns:
            Repsonse: 400 - duplicate username or email
                            create unsuccessful
                      200 - successful created a user
        """
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("username")
        password = data.get("password")
        first_name = data.get("firstname")
        last_name = data.get("lastname")
        email = data.get("email")
        # Sign up required fieldss
        if first_name and last_name and username and password and email:

            # User or email exist in the db already, refuse registration
            if (
                Client.objects.filter(username=username).exists()
                or Client.objects.filter(email=email).exists()
            ):
                return Response(
                    status=400,
                    data={"Error": "Username or email already exist"},
                )

            Client.objects.create_user(
                email=email,
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            return Response(
                status=200,
                data={"success": f"client {username} created"},
            )
        else:
            return Response(
                status=400,
                data={"Error": "Missing required field for createing account"},
            )

    def delete(self, request, pk):

        client = get_object_or_404(Client, pk=pk)
        client.delete()

        return Response(
            status=200, data={"Message": f"Client {pk} is deleted successfully"}
        )


class ClientListView(APIView):
    def get(self, request):
        users = Client.objects.all()
        serializer = ClientSerializer(users, many=True)
        return Response(serializer.data)


class SignInView(APIView):
    def post(self, request):
        """check usernae and password to signin

        Args:
            request (_type_): POST
            with username and password
        """
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            Response(status=200, data={"message": f"{username} log in successfule"})
        else:
            # Unauthorized client 401
            Response(status=401, data={"message": "Invalid username or password"})
