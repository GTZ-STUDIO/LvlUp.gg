from django.urls import path
from .views import *

urlpatterns = [
    path("create_blog/", Blogs.as_view()),
    path("getlist/", Blogs.as_view()),
    path("delete_blog/<int:pk>/", Blogs.as_view()),
    path("get_blog/", GetBlogs.as_view()),
    path("update_blog/<int:pk>/", Blogs.as_view()),
    path("likes/<int:pk>/", GetBlogs.as_view()),
    path("recommended/", reccomendedBlogs.as_view())
]