
# accounts/urls.py
from django.urls import path

from .views import ClientDetailView, ClientListView, SignInView

urlpatterns = [
    path("", ClientListView.as_view()),
    path("signup/", ClientDetailView.as_view()),
    path("signin/", SignInView().as_view()),
]

