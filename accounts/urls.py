from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("new-client", views.new_client, name="new-client"),
    path("new-business", views.new_business, name="new-business"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
]