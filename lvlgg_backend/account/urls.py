# accounts/urls.py
from django.urls import path
from .views import SignUpView, UserListView

urlpatterns = [
    path("", UserListView.as_view()),
    path("signup/", SignUpView.as_view()),
]
