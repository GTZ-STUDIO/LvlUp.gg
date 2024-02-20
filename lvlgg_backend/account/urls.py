# accounts/urls.py
from django.urls import path, re_path

from .views import ClientDetailView, ClientListView, SignInView

urlpatterns = [
    path("", ClientListView.as_view()),
    path("delete/<int:pk>/", ClientDetailView.as_view()),
    path("<int:pk>/", ClientDetailView.as_view()),
    path("update/<int:pk>/", ClientDetailView.as_view()),
    path("signup/", ClientDetailView.as_view()),
    path("signin/", SignInView.as_view()),
]
