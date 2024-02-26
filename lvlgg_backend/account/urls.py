# accounts/urls.py
from django.urls import path, re_path

from .views import ClientDetailView, ClientListView, SignInView

urlpatterns = [
    path("signout/", ClientDetailView.as_view(), name="sign_out"),
    path("", ClientListView.as_view(), name="user_list"),
    path("delete/<int:pk>/", ClientDetailView.as_view()),
    path("<int:pk>/", ClientDetailView.as_view()),
    path("update/<int:pk>/", ClientDetailView.as_view(), name="update"),
    path("signup/", ClientDetailView.as_view(), name="sign_up"),
    path("signin/", SignInView.as_view()),
]
