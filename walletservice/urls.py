from django.urls import path, include
from . import views
urlpatterns = [
    path("", views.Wallets.as_view(), name="wallets"),
    path("transactions/", views.Transactions.as_view(), name="transactions")
]
