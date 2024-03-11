from account.models import Client
from blog.models import Blog
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Favourite
from .serializers import FavouriteSerializer


class FavouriteBlogsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        TODO: Double check if the favourite needed a get
              request

        Args:
            request (_type_): _description_
        """
        pass

    def post(self, request, blog_pk):

        client = request.user
        blog = get_object_or_404(Blog, pk=blog_pk)

        # Check if the blog is already favourited by the client
        if Favourite.objects.filter(client=client, blog=blog).exists():
            return Response(
                {"detail": "Blog is already favorited by the client."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create a new favourite relationship
        favourite_blog = Favourite.objects.create(client=client, blog=blog)
        serializer = FavouriteSerializer(favourite_blog)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FavouriteBlogsListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavouriteSerializer

    def get_queryset(self):
        """
        Get client's list of favourite blogs

        Returns:
            A list of favourite blogs
            200: Success
            403: Unauthorized
        """
        favourite = Favourite.objects.all()
        client = self.request.user
        client_favourite = favourite.filter(client=client)
        return client_favourite
