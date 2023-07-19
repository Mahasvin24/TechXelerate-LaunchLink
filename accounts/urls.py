from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("new-client", views.new_client, name="new-client"),
    path("new-business", views.new_business, name="new-business"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("volunteers/<int:volunteer_id>", views.volunteer_profile, name="volunteer-profile"),
    path("clients/<int:client_id>", views.client_profile, name="client-profile"),
    path("business/<int:business_id>", views.business_profile, name="business-profile"),
]