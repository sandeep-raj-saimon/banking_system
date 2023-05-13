from django.urls import path, include
from . import views
urlpatterns = [
    path("", views.Wallets.as_view(), name="get_wallets")
]
