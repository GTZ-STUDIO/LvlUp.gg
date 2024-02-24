import json

from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Client
from .serializer import ClientSerializer

# Create your views here.


class ClientDetailView(APIView):
    # TODO: update user info
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

        data = request.data

        username = data.get("username")
        password = data.get("password")
        firstname = data.get("firstname")
        lastname = data.get("lastname")
        email = data.get("email")
        # Sign up required fieldss
        if firstname and lastname and username and password and email:

            # User or email exist in the db already, refuse registration
            if (
                Client.objects.filter(username=username).exists()
                or Client.objects.filter(email=email).exists()
            ):
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"Error": "Username or email already exist"},
                )

            Client.objects.create_user(
                email=email,
                username=username,
                password=password,
                firstname=firstname,
                lastname=lastname,
            )
            return Response(
                status=status.HTTP_200_OK,
                data={"success": f"client {username} created"},
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"Error": "Missing required field for creating account"},
            )

    def delete(self, request, pk):
        """
        Delete a user based on pk

        Args:
            request (_type_): http request with pk in url
            pk (_type_): primary key

        Returns:
            DRF response, 200 for success, 404 for client does not exist
        """
        client = get_object_or_404(Client, pk=pk)
        client.delete()

        return Response(
            status=status.HTTP_200_OK,
            data={"Message": f"Client {pk} is deleted successfully"},
        )

    def get(self, request, pk):
        """
        retrieve a user based on pk

        Args:
            request (_type_): http request with pk in url
            pk (_type_): primary key

        Returns:
            DRF response, 200 for success or 404 for client does not exist
        """
        client = get_object_or_404(Client, pk=pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, pk):
        data = request.data

        client = get_object_or_404(Client, pk=pk)
        serializer = ClientSerializer(client, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                status=status.HTTP_200_OK, data={"Message": "Update successful"}
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={"Error": serializer.errors},
        )


class ClientListView(APIView):
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)


class SignInView(APIView):

    def post(self, request):
        """check usernae and password to signin

        Args:
            request (_type_): POST
            with username and password

        Return:
            200: successful
            401: Unauthorize, invalid username or password
        """

        data = request.data
        username = data.get("username")
        password = data.get("password")

        # username and password are madatory
        if not username or not password:
            return Response(status=400, data={"Error": "Missing username or password"})

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(
                status=200, data={"message": f"{username} log in successfully"}
            )
        else:
            # Unauthorized client 401
            return Response(
                status=401, data={"message": "Incorrect username or password"}
            )
