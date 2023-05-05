from django.urls import path, include
from . import views
urlpatterns = [
    path("", views.User.as_view(), name="get_users"),
    path("logout/", views.Logout.as_view(), name="logout")
]
