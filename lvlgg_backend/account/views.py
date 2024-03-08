from blog.models import Blog
from comment.models import Comment
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Client
from .serializer import ClientSerializer


class ClientDetailView(APIView):
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
        try:
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
        except ValidationError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"Error": "Invalid Email Format"},
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
        if not request.user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"Error": "Please log in first to proceed."},
            )
        client = get_object_or_404(Client, pk=pk)
        if client.username != request.user.username:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"Error": "You cannot delete other user's profile"},
            )
        client.delete()

        return Response(
            status=status.HTTP_200_OK,
            data={"Message": f"Client {pk} is deleted successfully"},
        )

    def get(self, request, pk=None):
        """
        retrieve a client based on pk
        or if pk is not provided, it is a log out request
        Args:
            request (_type_): http request with pk in url
            pk (_type_): primary key

        Returns:
            DRF response, 200 for success or 404 for client does not exist
        """

        # use pk to retrieve a client
        if pk != None:
            if not request.user.is_authenticated:
                return Response(
                    status=status.HTTP_403_FORBIDDEN,
                    data={"Error": "Please log in first to proceed."},
                )
            client = get_object_or_404(Client, pk=pk)
            serializer = ClientSerializer(client)
            return Response(serializer.data)
        else:
            logout(request=request)
            return Response(
                status=status.HTTP_200_OK, data={"message": "Log out successfully"}
            )

    def put(self, request, pk):
        if not request.user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"Error": "Please log in first to proceed."},
            )
        data = request.data

        client = get_object_or_404(Client, pk=pk)
        if client.username != request.user.username:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"Error": "You can only change your own user profile"},
            )

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


class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


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
            user = get_object_or_404(Client, username=username)
            serializer = ClientSerializer(user)
            return Response(status=200, data=serializer.data)
        else:
            # Unauthorized client 401
            return Response(
                status=401,
                data={
                    "message": "The username and password provided does not match with any user"
                },
            )


class FollowFriendView(APIView):
    def post(self, request):
        """
        Add a client as a friend

        Args:
            request: request is account/friend with a payload
                     {"username":"Friend's username"}

        Returns:
            200: success
            400: payload does does contain any username
            404: no such user under that username
            403: request user is not authenticated
        """
        if not request.user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"Error": "Please log in first to proceed."},
            )

        data = request.data

        username = data.get("username")

        # Return 400 if missing username in the payload
        if not username:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"Error": "Missing friend's username"},
            )

        client = get_object_or_404(Client, pk=request.user.id)
        friend = get_object_or_404(Client, username=username)

        client.friends.add(friend)
        return Response(
            status=status.HTTP_200_OK,
            data={"Message": f"{friend.username} has been added to the friend list"},
        )


class RemoveFriendView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"Error": "Please log in first to proceed."},
            )

        data = request.data

        username = data.get("username")

        # Return 400 if missing username in the payload
        if not username:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"Error": "Missing friend's username"},
            )

        client = get_object_or_404(Client, pk=request.user.id)
        friend = get_object_or_404(Client, username=username)

        client.friends.remove(friend)
        return Response(
            status=status.HTTP_200_OK,
            data={
                "Message": f"{friend.username} has been removed from the friend list"
            },
        )


class FriendListView(generics.ListAPIView):
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        client = self.request.user
        return client.friends.all()
