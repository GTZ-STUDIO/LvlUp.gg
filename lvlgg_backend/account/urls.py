# accounts/urls.py
from django.urls import path, re_path

from .views import (
    ClientDetailView,
    ClientListView,
    FollowFriendView,
    FriendBlogsView,
    FriendListView,
    RemoveFriendView,
    SignInView,
)

urlpatterns = [
    path("signout/", ClientDetailView.as_view(), name="sign_out"),
    path("", ClientListView.as_view(), name="user_list"),
    path("delete/<int:pk>/", ClientDetailView.as_view()),
    path("<int:pk>/", ClientDetailView.as_view()),
    path("update/<int:pk>/", ClientDetailView.as_view(), name="update"),
    path("signup/", ClientDetailView.as_view(), name="sign_up"),
    path("signin/", SignInView.as_view(), name="sign_in"),
    path("follow/", FollowFriendView.as_view(), name="add_friend"),
    path("unfollow/", RemoveFriendView.as_view(), name="remove_friend"),
    path("friends/", FriendListView.as_view(), name="friend_list"),
    path("friend/<str:username>/blogs", FriendBlogsView.as_view(), name="friend_blog"),
]
