# accounts/urls.py
from django.urls import path
from .views import BlogDetailView

urlpatterns = [
    path("blog/", BlogDetailView.as_view()),
]
