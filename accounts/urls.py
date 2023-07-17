from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("new-client", views.new_client, name="new-client"),
]