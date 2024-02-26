from django.urls import path
from .views import *

urlpatterns = [
    path("create_comment/", Comments.as_view()),
    path("get_comments/<int:blog_Id>/", Comments.as_view()),
    path("delete_comment/<int:pk>/", Comments.as_view()),
    path("get_comment/<int:pk>/", Comments.as_view()),
    path("update_comment/<int:pk>/", Comments.as_view()),
]