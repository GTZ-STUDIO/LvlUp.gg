from django.urls import path, re_path

from .views import FavouriteBlogsListView, FavouriteBlogsView

urlpatterns = [
    path("list/", FavouriteBlogsListView.as_view(), name="favourite_list"),
    path(
        "subscribe/<int:blog_pk>/", FavouriteBlogsView.as_view(), name="add_favourite"
    ),
    path(
        "unsubscribe/<int:blog_pk>/",
        FavouriteBlogsView.as_view(),
        name="remove_favourite",
    ),
]
